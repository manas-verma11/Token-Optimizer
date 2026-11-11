
import re

NEGATION_WORDS = {
    "not", "no", "never", "cannot", "can't",
    "don't", "doesn't", "won't", "shouldn't",
    "couldn't", "wouldn't", "isn't", "aren't",
    "wasn't", "weren't", "didn't", "hasn't",
    "haven't", "hadn't"
}

MODAL_WORDS = {
    "must", "may", "might", "should", "could",
    "would", "shall", "will", "can"
}

CONSTRAINT_PHRASES = {
    "at least", "at most", "only", "unless",
    "before", "after", "exactly", "minimum",
    "maximum", "no more than", "no less than",
    "greater than", "less than"
}


def extract_negation_words(text):
    words = re.findall(r"\b[\w']+\b", text.lower())
    return {word for word in words if word in NEGATION_WORDS}


def preserves_negation(original_text, candidate_text):
    return extract_negation_words(original_text).issubset(
        extract_negation_words(candidate_text)
    )


def extract_modal_words(text):
    words = re.findall(r"\b[\w']+\b", text.lower())
    return {word for word in words if word in MODAL_WORDS}


def extract_numbers_and_dates(text):
    pattern = (
        r"\b\d+(?:,\d{3})*(?:\.\d+)?"
        r"(?:%|[A-Za-z]{1,5})?\b"
        r"|₹\s?\d+(?:,\d{3})*(?:\.\d+)?"
        r"|\$\s?\d+(?:,\d{3})*(?:\.\d+)?"
    )
    return set(re.findall(pattern, text))


def extract_constraints(text):
    text = text.lower()
    found = set()

    for phrase in CONSTRAINT_PHRASES:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if re.search(pattern, text):
            found.add(phrase)

    return found


def extract_identifiers(text):
    # Protect technical identifiers such as userId, API_KEY and user_id.
    pattern = r"\b(?:[A-Z][A-Z0-9_]{1,}|[a-z]+[A-Z][A-Za-z0-9]*|[a-zA-Z]+_[a-zA-Z0-9_]+)\b"
    return set(re.findall(pattern, text))


def validate_semantics(original_text, candidate_text):
    checks = {
        "negation": (
            extract_negation_words(original_text),
            extract_negation_words(candidate_text)
        ),
        "modal_words": (
            extract_modal_words(original_text),
            extract_modal_words(candidate_text)
        ),
        "numbers_and_dates": (
            extract_numbers_and_dates(original_text),
            extract_numbers_and_dates(candidate_text)
        ),
        "constraints": (
            extract_constraints(original_text),
            extract_constraints(candidate_text)
        ),
        "identifiers": (
            extract_identifiers(original_text),
            extract_identifiers(candidate_text)
        )
    }

    failed_checks = []

    for check_name, (original, candidate) in checks.items():
        if not original.issubset(candidate):
            failed_checks.append(check_name)

    return {
        "is_safe": len(failed_checks) == 0,
        "failed_checks": failed_checks
    }
