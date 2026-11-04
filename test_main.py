from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_count_tokens():
    response = client.post("/count-tokens", json={"text": "Hello world"})

    assert response.status_code == 200
    assert response.json()["text"]=="Hello world"
    assert response.json()["token_count"] == 2


def test_empty_text():
    response = client.post("/count-tokens", json={"text": ""})

    assert response.status_code == 422

def test_missing_text():
    response = client.post("/count-tokens", json={})
    
    assert response.status_code == 422

def test_optimize_text():
    response = client.post(
        "/optimize",
        json={"text": "Python is useful.\nToken optimization saves money.\nPython is useful."}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["optimized_text"] == ("Python is useful.\nToken optimization saves money.")

    assert data["tokens_saved"] == (data["original_token_count"] - data["optimized_token_count"])

    assert data["savings_Percentage"] >=0


def test_optimize_empty_text():
    response = client.post(
        "/optimize",
        json={"text": ""}
    )

    assert response.status_code == 422

def test_create_session():
    response = client.post("/sessions")

    assert response.status_code == 201

    data = response.json()

    assert "session_id" in data
    assert "started_at" in data
    assert "expires_at" in data
    assert data["status"] == "active"


def test_missing_session_history():
    response = client.get("/sessions/nonexistent-session-id/history")

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_active_session_history():
    create_response = client.post("/sessions")

    session_id = create_response.json()["session_id"]

    response = client.get(f"/sessions/{session_id}/history")

    assert response.status_code == 200
    assert response.json()["session_id"] == session_id
    assert response.json()["messages"] == []


def test_expired_session_history():
    from session_database import get_session_connection

    create_response = client.post("/sessions")
    session_id = create_response.json()["session_id"]

    connection = get_session_connection()

    connection.execute(
        "UPDATE conversation_sessions SET expires_at = ? WHERE session_id = ?",
        ("2026-11-04T00:00:00+00:00", session_id)
    )

    connection.commit()
    connection.close()

    response = client.get(f"/sessions/{session_id}/history")

    assert response.status_code == 410
    assert response.json()["detail"] == "Session has expired. Start a new session."


def test_expired_session_generates_report_and_deletes_messages():
    from session_database import get_session_connection, get_session_report
    from session_service import save_conversation_message

    session_id = client.post("/sessions").json()["session_id"]

    save_conversation_message(
        session_id,
        "user",
        "Test message before expiry"
    )

    connection = get_session_connection()

    connection.execute(
        "UPDATE conversation_sessions SET expires_at = ? WHERE session_id = ?",
        ("2026-11-04T00:00:00+00:00", session_id)
    )

    connection.commit()
    connection.close()

    response = client.get(f"/sessions/{session_id}/history")

    assert response.status_code == 410

    report = get_session_report(session_id)

    assert report is not None
    assert report["session_id"] == session_id
    assert report["total_messages"] == 1

    connection = get_session_connection()

    message_count = connection.execute(
        "SELECT COUNT(*) FROM conversation_messages WHERE session_id = ?",
        (session_id,)
    ).fetchone()[0]

    connection.close()

    assert message_count == 0
