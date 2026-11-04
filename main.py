from fastapi import FastAPI, HTTPException
from schemas import TokenRequest, OptimizeRequest, SessionResponse, SessionStatusResponse, SessionPromptRequest
from token_counter import count_tokens
from optimization_service import optimize_text
from statistics_tracker import record_optimization, get_statistics, reset_statistics
from database import initialize_database, save_optimization, get_optimization_history
from session_service import start_new_session, get_session_status, get_conversation_history, process_session_prompt
from session_database import (
    initialize_session_database,
    get_session_report,
    get_all_session_reports
)


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Token optimizer api is running"}

@app.post("/count-tokens")
def count_tokens_endpoint(request: TokenRequest):
    count = count_tokens(request.text)

    return{
        "text": request.text,
        "token_count": count
    }

@app.post("/optimize")
def optimize_text_endpoint(request: TokenRequest):
    return optimize_text(request.text)

@app.post("/optimize-text")
def optimize_text_endpoint(request: OptimizeRequest):
    try:
        result = optimize_text(request.text, request.model_name)
        record_optimization(result)
        save_optimization(result)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/statistics")
def statistics_endpoint():
    return get_statistics()

@app.delete("/statistics")
def reset_statistics_endpoint():
    reset_statistics()

    return{
        "message": "Statistics reset successfully",
        "statistics": get_statistics()
    }

@app.on_event("startup")
def startup_event():
    initialize_database()
    initialize_session_database()


@app.get("/history")
def optimization_history_endpoint(limit: int = 50):
    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=400, 
            detail="Limit must be between 1 and 500"
        )

    return get_optimization_history(limit)

@app.get("/session-reports")
def session_reports_endpoint(limit: int = 50):
    try:
        return get_all_session_reports(limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/session-reports/{session_id}")
def single_session_report_endpoint(session_id: str):
    report = get_session_report(session_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Session report not found"
        )   

    return report

@app.post("/sessions", response_model=SessionResponse, status_code=201)
def create_session_endpoint():
    return start_new_session()

@app.get("/sessions/{session_id}", response_model=SessionStatusResponse)
def session_status_endpoint(session_id: str):
    try:
        return get_session_status(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.get("/sessions/{session_id}/history")
def session_history_endpoint(session_id: str):
    try:
        return {
            "session_id": session_id,
            "messages": get_conversation_history(session_id)
        }
    except ValueError as exc:
        if "not found" in str(exc).lower():
            raise HTTPException(status_code=404, detail=str(exc))

        raise HTTPException(status_code=410, detail=str(exc))

@app.post("/sessions/{session_id}/optimize")
def session_optimize_endpoint(
    session_id: str,
    request: SessionPromptRequest
):
    try:
        return process_session_prompt(
            session_id,
            request.text,
            request.model_name
        )
    except ValueError as exc:
        if "not found" in str(exc).lower():
            raise HTTPException(status_code=404, detail=str(exc))

        raise HTTPException(status_code=410, detail=str(exc))   