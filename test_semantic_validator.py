
from semantic_validator import (
    extract_negation_words,
    preserves_negation
)


def test_extract_negation_words():
    result = extract_negation_words("I do not agree.")
    assert result == {"not"}


def test_reject_candidate_when_not_is_removed():
    assert preserves_negation(
        "I do not agree.",
        "I agree."
    ) is False


def test_accept_candidate_when_negation_is_preserved():
    assert preserves_negation(
        "I do not agree.",
        "I do not agree."
    ) is True


def test_accept_text_without_negation():
    assert preserves_negation(
        "This is useful.",
        "This is helpful."
    ) is True


def test_detect_multiple_negations():
    result = extract_negation_words(
        "I never said I cannot do this."
    )
    assert result == {"never", "cannot"}


def test_reject_candidate_when_never_is_removed():
    assert preserves_negation(
        "I never agreed.",
        "I agreed."
    ) is False

from semantic_validator import validate_semantics


def test_reject_candidate_when_modal_verb_changes():
    result = validate_semantics(
        "You must restart the server.",
        "You may restart the server."
    )

    assert result["is_safe"] is False
    assert "modal_words" in result["failed_checks"]


def test_reject_candidate_when_number_changes():
    result = validate_semantics(
        "Transfer ₹50,000 today.",
        "Transfer ₹40,000 today."
    )

    assert result["is_safe"] is False
    assert "numbers_and_dates" in result["failed_checks"]


def test_reject_candidate_when_constraint_changes():
    result = validate_semantics(
        "Complete at least 5 tasks.",
        "Complete at most 5 tasks."
    )

    assert result["is_safe"] is False
    assert "constraints" in result["failed_checks"]


def test_reject_candidate_when_identifier_changes():
    result = validate_semantics(
        "Use API_KEY for authentication.",
        "Use API_TOKEN for authentication."
    )

    assert result["is_safe"] is False
    assert "identifiers" in result["failed_checks"]