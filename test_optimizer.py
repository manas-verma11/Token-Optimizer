from optimizer import remove_duplicate_lines
from optimizer import normalize_whitespace
from optimizer import remove_duplicate_sentences
from optimizer import remove_repeated_phrases
from optimizer import shorten_common_expressions

def test_remove_duplicate_lines():
    text = "Apple\nBanana\nApple"
    result = remove_duplicate_lines(text)

    assert result == "Apple\nBanana"

def test_preserve_words():
    text = "Apple\nBanana\nOrange\nApple"
    result = remove_duplicate_lines(text)

    assert result == "Apple\nBanana\nOrange"

def test_empty_text():

    assert remove_duplicate_lines("") == ""

def test_case_sensitivity():
    text = "Apple\napple"
    result = remove_duplicate_lines(text)

    assert result == "Apple\napple"

def test_normalize_multiple_spaces():
    text = "Hello     world"
    assert normalize_whitespace(text) == "Hello world"


def test_normalize_multiple_blank_lines():
    text = "Hello\n\n\n\nWorld"
    assert normalize_whitespace(text) == "Hello\n\nWorld"


def test_normalize_empty_text():
    assert normalize_whitespace("") == ""


def test_normalize_preserves_words():
    text = "Token optimization saves money"
    assert normalize_whitespace(text) == text

def test_remove_duplicate_sentences():
    text = (
        "Hello world. "
        "Python is useful. "
        "Hello world."
    )

    result = remove_duplicate_sentences(text)

    assert result == "Hello world. Python is useful."


def test_remove_duplicate_sentences_case_insensitive():
    text = "Hello world. HELLO WORLD."

    result = remove_duplicate_sentences(text)

    assert result == "Hello world."


def test_remove_duplicate_sentences_preserve_order():
    text = "Apple is good. Banana is good. Apple is good."

    result = remove_duplicate_sentences(text)

    assert result == "Apple is good. Banana is good."


def test_remove_duplicate_sentences_empty_text():
    assert remove_duplicate_sentences("") == ""


def test_remove_duplicate_sentences_multiple_lines():
    text = "Hello world.\nPython is useful.\nHello world."

    result = remove_duplicate_sentences(text)

    assert result == "Hello world. Python is useful."

def test_remove_repeated_phrases():
    text = "Explain token optimization token optimization clearly."

    result = remove_repeated_phrases(text)

    assert result == "Explain token optimization clearly."


def test_remove_repeated_phrases_case_insensitive():
    text = "Learn Python Learn python today."

    result = remove_repeated_phrases(text)

    assert result == "Learn Python today."


def test_remove_repeated_phrases_empty_text():
    assert remove_repeated_phrases("") == ""


def test_remove_repeated_phrases_preserves_non_repeated_text():
    text = "Explain token optimization clearly."

    assert remove_repeated_phrases(text) == text


def test_remove_repeated_phrases_preserves_single_word_repetition():
    text = "This is very very important."

    assert remove_repeated_phrases(text) == text

def test_shorten_in_order_to():
    assert shorten_common_expressions("In order to learn.") == "To learn."


def test_shorten_make_use_of():
    assert shorten_common_expressions("Make use of Python.") == "Use Python."


def test_shorten_due_to_the_fact_that():
    assert shorten_common_expressions(
        "Due to the fact that it rained, we stayed home."
    ) == "Because it rained, we stayed home."


def test_shorten_at_this_point_in_time():
    assert shorten_common_expressions(
        "At this point in time, we should stop."
    ) == "Now, we should stop."


def test_shorten_for_the_purpose_of():
    assert shorten_common_expressions(
        "For the purpose of testing, run this."
    ) == "For testing, run this."


def test_shorten_common_expressions_empty_text():
    assert shorten_common_expressions("") == ""


def test_shorten_common_expressions_preserves_unmatched_text():
    text = "Python is useful for backend development."
    assert shorten_common_expressions(text) == text


def test_shorten_common_expressions_matches_case_insensitively():
    assert shorten_common_expressions(
        "IN ORDER TO learn."
    ) == "TO learn."


def test_shorten_common_expressions_does_not_match_partial_words():
    text = "We need to make use of the tool."
    result = shorten_common_expressions(text)
    assert result == "We need to use the tool."

def test_shorten_at_the_present_time():
    assert shorten_common_expressions(
        "At the present time, the system is running."
    ) == "Now, the system is running."


def test_shorten_in_the_near_future():
    assert shorten_common_expressions(
        "We will deploy in the near future."
    ) == "We will deploy soon."


def test_shorten_in_the_event_that():
    assert shorten_common_expressions(
        "In the event that it fails, retry."
    ) == "If it fails, retry."


def test_shorten_despite_the_fact_that():
    assert shorten_common_expressions(
        "Despite the fact that it rained, we continued."
    ) == "Although it rained, we continued."


def test_shorten_on_a_daily_basis():
    assert shorten_common_expressions(
        "Run the backup on a daily basis."
    ) == "Run the backup daily."


def test_shorten_on_a_regular_basis():
    assert shorten_common_expressions(
        "Check the logs on a regular basis."
    ) == "Check the logs regularly."