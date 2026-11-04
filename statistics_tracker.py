
_statistics = {
    "total_requests": 0,
    "improved_requests": 0,
    "unchanged_requests": 0,
    "total_tokens_saved": 0,
    "total_cost_saved": 0.0,
}


def record_optimization(result):
    _statistics["total_requests"] += 1

    if result["optimization_status"] == "improved":
        _statistics["improved_requests"] += 1
    else:
        _statistics["unchanged_requests"] += 1

    _statistics["total_tokens_saved"] += result["tokens_saved"]
    _statistics["total_cost_saved"] += result["estimated_cost_saved"]


def get_statistics():
    total = _statistics["total_requests"]

    if total == 0:
        improvement_rate = 0.0
    else:
        improvement_rate = (
            _statistics["improved_requests"] / total
        ) * 100

    return {
        **_statistics,
        "improvement_rate_percentage": round(improvement_rate, 2),
    }


def reset_statistics():
    for key in _statistics:
        _statistics[key] = 0
