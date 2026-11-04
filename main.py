from fastapi import FastAPI, HTTPException
from schemas import TokenRequest, OptimizeRequest, SessionResponse
from token_counter import count_tokens
from optimization_service import optimize_text
from statistics_tracker import record_optimization, get_statistics, reset_statistics
from database import initialize_database, save_optimization, get_optimization_history
from session_database import get_session_report, get_all_session_reports
from session_service import start_new_session


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

@app.post("/session", response_model=SessionResponse, status_code=201)
def create_session_endpoint():
    return start_new_session()