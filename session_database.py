import uuid
import sqlite3
from datetime import datetime, timedelta, timezone

from database import DATABASE_NAME


SESSION_DURATION_MINUTES = 5


def get_session_connection():
    """Create a SQLite connection for session management."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_session_database():
    """Create tables required for conversation sessions."""

    connection = get_session_connection()
    cursor = connection.cursor()

    # Stores session metadata and aggregate metrics.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_sessions (
            session_id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            total_original_tokens INTEGER NOT NULL DEFAULT 0,
            total_optimized_tokens INTEGER NOT NULL DEFAULT 0,
            total_tokens_saved INTEGER NOT NULL DEFAULT 0,
            total_cost_saved REAL NOT NULL DEFAULT 0,
            total_messages INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Stores temporary conversation messages.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id)
                REFERENCES conversation_sessions(session_id)
                ON DELETE CASCADE
        )
    """)

    # Stores permanent session summaries.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            started_at TEXT NOT NULL,
            ended_at TEXT NOT NULL,
            total_messages INTEGER NOT NULL,
            total_original_tokens INTEGER NOT NULL,
            total_optimized_tokens INTEGER NOT NULL,
            total_tokens_saved INTEGER NOT NULL,
            savings_percentage REAL NOT NULL,
            total_cost_saved REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_session():
    """Create a new conversation session with a fixed 5-minute lifetime."""

    connection = get_session_connection()
    cursor = connection.cursor()

    started_at = datetime.now(timezone.utc)
    expires_at = started_at + timedelta(
        minutes=SESSION_DURATION_MINUTES
    )

    session_id = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO conversation_sessions (
            session_id,
            started_at,
            expires_at,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        started_at.isoformat(),
        expires_at.isoformat(),
        "active"
    ))

    connection.commit()
    connection.close()

    return {
        "session_id": session_id,
        "started_at": started_at.isoformat(),
        "expires_at": expires_at.isoformat(),
        "status": "active"
    }

def is_session_expired(session_id, now=None):
    """Check whether a session has reached its expiration time."""

    connection = get_session_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT expires_at, status
        FROM conversation_sessions
        WHERE session_id = ?
    """, (session_id,))

    session = cursor.fetchone()
    connection.close()

    if session is None:
        raise ValueError("Session not found")

    if session["status"] != "active":
        return True

    expires_at = datetime.fromisoformat(session["expires_at"])

    if now is None:
        now = datetime.now(timezone.utc)

    return now >= expires_at

def save_message(session_id, role, content):
    """Save a temporary conversation message."""

    if role not in ("user", "assistant", "system"):
        raise ValueError("Invalid message role")

    if is_session_expired(session_id):
        raise ValueError("Cannot save a message to an expired session")

    connection = get_session_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversation_messages (
            session_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        role,
        content,
        datetime.now(timezone.utc).isoformat()
    ))

    cursor.execute("""
        UPDATE conversation_sessions
        SET total_messages = total_messages + 1
        WHERE session_id = ?
    """, (session_id,))

    connection.commit()
    connection.close()


def get_session_messages(session_id):
    """Retrieve conversation history if the session is still active."""

    # Always check expiration BEFORE retrieving conversation history.
    if is_session_expired(session_id):
        raise ValueError("Session has expired. Conversation history is unavailable.")

    connection = get_session_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, content, created_at
        FROM conversation_messages
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,))

    messages = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return messages

def record_session_optimization(
    session_id,
    original_tokens,
    optimized_tokens,
    cost_saved
):
    """Add one optimization's metrics to the session totals."""

    if original_tokens < 0 or optimized_tokens < 0 or cost_saved < 0:
        raise ValueError("Optimization metrics cannot be negative")

    if optimized_tokens > original_tokens:
        raise ValueError("Optimized tokens cannot exceed original tokens")

    connection = get_session_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT expires_at, status
        FROM conversation_sessions
        WHERE session_id = ?
    """, (session_id,))

    session = cursor.fetchone()

    if session is None:
        connection.close()
        raise ValueError("Session not found")

    expires_at = datetime.fromisoformat(session["expires_at"])

    if session["status"] != "active" or datetime.now(timezone.utc) >= expires_at:
        connection.close()
        raise ValueError("Cannot update an expired or completed session")

    tokens_saved = original_tokens - optimized_tokens

    cursor.execute("""
        UPDATE conversation_sessions
        SET
            total_original_tokens = total_original_tokens + ?,
            total_optimized_tokens = total_optimized_tokens + ?,
            total_tokens_saved = total_tokens_saved + ?,
            total_cost_saved = total_cost_saved + ?
        WHERE session_id = ?
    """, (
        original_tokens,
        optimized_tokens,
        tokens_saved,
        cost_saved,
        session_id
    ))

    connection.commit()
    connection.close()

def finalize_session(session_id, now=None):
    """Generate a permanent report and delete temporary messages."""

    if now is None:
        now = datetime.now(timezone.utc)

    connection = get_session_connection()
    cursor = connection.cursor()

    try:
        # 1. Retrieve session information.
        cursor.execute("""
            SELECT *
            FROM conversation_sessions
            WHERE session_id = ?
        """, (session_id,))

        session = cursor.fetchone()

        if session is None:
            raise ValueError("Session not found")

        if session["status"] != "active":
            raise ValueError("Session is already completed")

        # 2. Check whether the session has expired.
        expires_at = datetime.fromisoformat(session["expires_at"])

        if now < expires_at:
            raise ValueError("Cannot finalize an active session")

        # 3. Calculate overall savings percentage.
        original_tokens = session["total_original_tokens"]
        optimized_tokens = session["total_optimized_tokens"]
        tokens_saved = session["total_tokens_saved"]

        if original_tokens > 0:
            savings_percentage = (
                tokens_saved / original_tokens
            ) * 100
        else:
            savings_percentage = 0.0

        # 4. Prepare the permanent report.
        report = {
            "session_id": session_id,
            "started_at": session["started_at"],
            "ended_at": now.isoformat(),
            "total_messages": session["total_messages"],
            "total_original_tokens": original_tokens,
            "total_optimized_tokens": optimized_tokens,
            "total_tokens_saved": tokens_saved,
            "savings_percentage": round(savings_percentage, 2),
            "total_cost_saved": session["total_cost_saved"]
        }

        # 5. Save the permanent report.
        cursor.execute("""
            INSERT INTO session_reports (
                session_id,
                started_at,
                ended_at,
                total_messages,
                total_original_tokens,
                total_optimized_tokens,
                total_tokens_saved,
                savings_percentage,
                total_cost_saved
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            report["session_id"],
            report["started_at"],
            report["ended_at"],
            report["total_messages"],
            report["total_original_tokens"],
            report["total_optimized_tokens"],
            report["total_tokens_saved"],
            report["savings_percentage"],
            report["total_cost_saved"]
        ))

        # 6. Delete temporary conversation messages.
        cursor.execute("""
            DELETE FROM conversation_messages
            WHERE session_id = ?
        """, (session_id,))

        # 7. Mark the session as completed.
        cursor.execute("""
            UPDATE conversation_sessions
            SET status = 'completed'
            WHERE session_id = ?
        """, (session_id,))

        # 8. Commit all changes together.
        connection.commit()

        return report

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def get_session_report(session_id):
    """Retrieve the permanent report of a particular session."""

    connection = get_session_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM session_reports
        WHERE session_id = ?
    """, (session_id,))

    report = cursor.fetchone()
    connection.close()

    if report is None:
        return None

    return dict(report)

def get_all_session_reports(limit=50):
    """Retrieve historical session reports, newest first."""

    if limit < 1 or limit > 500:
        raise ValueError("Limit must be between 1 and 500")

    connection = get_session_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM session_reports
        ORDER BY report_id DESC
        LIMIT ?
    """, (limit,))

    reports = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return reports

