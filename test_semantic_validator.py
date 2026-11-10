
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
