from candidate_engine import select_best_candidate
from token_counter import count_tokens

def test_candidate_engine_returns_required_fields():
    result = select_best_candidate("Hello world.")

    assert "optimized_text" in result
    assert "selected_strategy" in result
    assert "optimized_token_count" in result


def test_original_is_selected_when_no_strategy_improves():
    text = "Hello world."

    result = select_best_candidate(text)

    assert result["optimized_text"] == text
    assert result["selected_strategy"] == "original"


def test_candidate_engine_does_not_increase_tokens():
    text = (
        "Token optimization saves money.\n"
        "Token optimization saves money.\n"
        "Token optimization saves money."
    )

    result = select_best_candidate(text)

    assert result["optimized_token_count"] <= count_tokens(text)

def test_candidate_engine_selects_repeated_phrase_removal():
    text = "Explain token optimization token optimization clearly."

    result = select_best_candidate(text)

    assert result["selected_strategy"] == "repeated_phrase_removal"
    assert result["optimized_text"] == "Explain token optimization clearly."
    assert result["optimized_token_count"] == 6

def test_candidate_engine_selects_common_expression_shortening():
    text = "In order to learn Python programming."

    result = select_best_candidate(text)

    assert result["selected_strategy"] == "common_expression_shortening"
    assert result["optimized_text"] == "To learn Python programming."
    assert result["optimized_token_count"] == 5

def test_candidate_engine_selects_filler_word_removal():
    text = "This is actually a useful project."

    result = select_best_candidate(text)

    assert result["selected_strategy"] == "filler_word_removal"
    assert result["optimized_text"] == "This is a useful project."
    assert result["optimized_token_count"] < count_tokens(text)

def test_candidate_engine_rejects_candidate_that_removes_negation():
    result = select_best_candidate(
        "I do not agree with this decision. "
        "I do not agree with this decision."
    )

    assert "not" in result["optimized_text"].lower()