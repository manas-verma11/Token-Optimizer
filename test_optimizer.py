from optimizer import remove_duplicate_lines
from optimizer import normalize_whitespace
from optimizer import remove_duplicate_sentences
from optimizer import remove_repeated_phrases

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