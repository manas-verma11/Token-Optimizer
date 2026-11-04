
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_optimize_text_with_valid_model():
    response = client.post(
        "/optimize-text",
        json={
            "text": (
                "Python is useful.\n"
                "Token optimization saves money.\n"
                "Python is useful."
            ),
            "model_name": "SampleLLM-Pro"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model_name"] == "SampleLLM-Pro"
    assert data["original_input_cost"] == 0.000104
    assert data["optimized_input_cost"] == 0.000072
    assert data["estimated_cost_saved"] == 0.000032


def test_optimize_text_with_invalid_model():
    response = client.post(
        "/optimize-text",
        json={
            "text": "Hello world",
            "model_name": "UnknownModel"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Unknown model: UnknownModel"


def test_statistics_updates_after_optimization():
    # Start with clean statistics
    client.delete("/statistics")

    response = client.post(
        "/optimize-text",
        json={
            "text": (
                "Token optimization saves money.\n"
                "Token optimization saves money.\n"
                "Token optimization saves money."
            ),
            "model_name": "SampleLLM"
        }
    )

    assert response.status_code == 200

    optimization_result = response.json()

    # Fetch updated statistics
    stats_response = client.get("/statistics")

    assert stats_response.status_code == 200

    stats = stats_response.json()

    assert stats["total_requests"] == 1
    assert stats["total_tokens_saved"] == optimization_result["tokens_saved"]

    # Clean up after the test
    client.delete("/statistics")


def test_statistics_reset_endpoint():
    # Create some statistics first
    client.post(
        "/optimize-text",
        json={
            "text": "Hello world.\nHello world.",
            "model_name": "SampleLLM"
        }
    )

    # Reset statistics
    reset_response = client.delete("/statistics")

    assert reset_response.status_code == 200
    assert reset_response.json()["message"] == "Statistics reset successfully"

    # Verify reset
    stats_response = client.get("/statistics")
    stats = stats_response.json()

    assert stats["total_requests"] == 0
    assert stats["improved_requests"] == 0
    assert stats["unchanged_requests"] == 0
    assert stats["total_tokens_saved"] == 0
    assert stats["total_cost_saved"] == 0.0
    assert stats["improvement_rate_percentage"] == 0.0