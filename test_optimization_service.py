import pytest
from optimization_service import optimize_text

def test_cost_fields_are_returned():
        text = (
                "Python is useful.\n"
                "Token optimization saves money.\n"
                "Python is useful."
        )

        result = optimize_text(text)

        assert "original_input_cost" in result
        assert "optimized_input_cost" in result
        assert "estimated_cost_saved" in result

        assert result["original_input_cost"] >= result["optimized_input_cost"]

        assert result["estimated_cost_saved"] == round(result["original_input_cost"] - result["optimized_input_cost"], 10)


def test_sample_llm_pricing():
    text = "Python is useful.\nPython is useful."

    result = optimize_text(text, "SampleLLM")

    assert result["model_name"] == "SampleLLM"
    assert result["original_input_cost"] == 0.000016
    assert result["optimized_input_cost"] == 0.000008


def test_sample_llm_pro_pricing():
    text = "Python is useful.\nPython is useful."

    result = optimize_text(text, "SampleLLM-Pro")

    assert result["model_name"] == "SampleLLM-Pro"
    assert result["original_input_cost"] == 0.000064
    assert result["optimized_input_cost"] == 0.000032

def test_unknown_model():
        with pytest.raises(ValueError, match="Unknown model"):
                optimize_text("Hello world", "UnknownModel")


def test_optmization_status_is_improved():
      text = (
            "Python is useful.\n"
            "Token optimization save money.\n"
            "Python is useful."
      )

      result = optimize_text(text)

      assert result["optimization_applied"] is True
      assert result["optimization_status"] == "improved"

def test_optimization_status_is_unchanged():
      text = "Python is useful."

      result = optimize_text(text)

      assert result["optimization_applied"] is False
      assert result["optimization_status"] == "unchanged"

      
def test_original_text_is_kept_if_optimization_increases_tokens(monkeypatch):
    import optimization_service

    original_text = "Original text"

    def fake_select_best_candidate(text):
        return {
            "optimized_text": "A longer optimized version",
            "selected_strategy": "duplicate_line_removal",
            "optimized_token_count": 5,
            "strategy_results": [
                {
                    "strategy": "original",
                    "token_count": 3,
                    "tokens_saved": 0,
                    "savings_percentage": 0
                },
                {
                    "strategy": "duplicate_line_removal",
                    "token_count": 5,
                    "tokens_saved": -2,
                    "savings_percentage": -66.67
                }
            ]
        }

    def fake_count_tokens(text):
        if text == original_text:
            return 3
        if text == "A longer optimized version":
            return 5
        raise AssertionError(f"Unexpected text: {text}")

    monkeypatch.setattr(
        optimization_service,
        "select_best_candidate",
        fake_select_best_candidate
    )

    monkeypatch.setattr(
        optimization_service,
        "count_tokens",
        fake_count_tokens
    )

    result = optimization_service.optimize_text(original_text)

    assert result["optimized_text"] == original_text
    assert result["optimized_token_count"] == 3
    assert result["selected_strategy"] == "original"
    assert result["tokens_saved"] == 0

