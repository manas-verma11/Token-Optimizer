
from statistics_tracker import (
    record_optimization,
    get_statistics,
    reset_statistics,
)


def test_statistics_for_improved_request():
    reset_statistics()

    result = {
        "optimization_status": "improved",
        "tokens_saved": 4,
        "estimated_cost_saved": 0.000008,
    }

    record_optimization(result)

    stats = get_statistics()

    assert stats["total_requests"] == 1
    assert stats["improved_requests"] == 1
    assert stats["unchanged_requests"] == 0
    assert stats["total_tokens_saved"] == 4
    assert stats["improvement_rate_percentage"] == 100.0


def test_statistics_for_unchanged_request():
    reset_statistics()

    result = {
        "optimization_status": "unchanged",
        "tokens_saved": 0,
        "estimated_cost_saved": 0.0,
    }

    record_optimization(result)

    stats = get_statistics()

    assert stats["total_requests"] == 1
    assert stats["improved_requests"] == 0
    assert stats["unchanged_requests"] == 1
    assert stats["improvement_rate_percentage"] == 0.0


def test_statistics_for_multiple_requests():
    reset_statistics()

    record_optimization({
        "optimization_status": "improved",
        "tokens_saved": 4,
        "estimated_cost_saved": 0.000008,
    })

    record_optimization({
        "optimization_status": "unchanged",
        "tokens_saved": 0,
        "estimated_cost_saved": 0.0,
    })

    record_optimization({
        "optimization_status": "improved",
        "tokens_saved": 3,
        "estimated_cost_saved": 0.000006,
    })

    stats = get_statistics()

    assert stats["total_requests"] == 3
    assert stats["improved_requests"] == 2
    assert stats["unchanged_requests"] == 1
    assert stats["total_tokens_saved"] == 7
    assert stats["improvement_rate_percentage"] == 66.67


def test_empty_statistics():
    reset_statistics()

    stats = get_statistics()
  
    assert stats["total_requests"] == 0
    assert stats["improvement_rate_percentage"] == 0.0
