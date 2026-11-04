from session_database import is_session_expired, finalize_session, create_session, get_session_messages, save_message, record_session_optimization
from datetime import datetime, timedelta, timezone
from optimization_service import optimize_text

def start_new_session():
    """Start a new conversation session."""
    session = create_session()

    return {
        "session_id": session["session_id"],
        "started_at": session["started_at"],
        "expires_at": session["expires_at"],
        "status": session["status"]
    }

def validate_session(session_id):
    """Validate whether a conversation session is active."""

    expired = is_session_expired(session_id)

    if expired:
        return False

    return True

def finalize_expired_session(session_id, now=None):
    """Finalize a session only if it has expired."""

    if not is_session_expired(session_id, now=now):
        return None

    report = finalize_session(session_id, now=now)

    return report

def get_conversation_history(session_id):
    """Retrieve the conversation history for a given session."""

    if not validate_session(session_id):
        raise ValueError("Session has expired. Start a new session.")

    return get_session_messages(session_id)

def save_conversation_message(session_id, role, content):
    """Validate and save a conversation message."""

    if not validate_session(session_id):
        raise ValueError("Session has expired. Start a new session.")
        
    save_message(session_id, role, content)

    return{
        "session_id": session_id,
        "role": role,
        "saved": True
    }

def process_session_prompt(session_id, user_prompt, model_name="SampleLLM"):
    """Process a user prompt within an active conversation session."""

    # 1. Validate the session
    if not validate_session(session_id):
        raise ValueError("Session has expired. Start a new session.")

    # 2. Retrieve previous conversation history
    conversation_history = get_conversation_history(session_id)

    # 3. Optimize the user's prompt
    optimization_result = optimize_text(
        user_prompt,
        model_name=model_name
    )

    # 4. Record optimization metrics
    record_session_optimization(
        session_id,
        optimization_result["original_token_count"],
        optimization_result["optimized_token_count"],
        optimization_result["estimated_cost_saved"]
    )

    # 5. Save the original user prompt
    save_conversation_message(
        session_id,
        "user",
        user_prompt
    )

    # 6. Save the optimized prompt
    save_conversation_message(
        session_id,
        "assistant",
        optimization_result["optimized_text"]
    )

    return {
        "session_id": session_id,
        "conversation_history": conversation_history,
        "optimization_result": optimization_result
    }