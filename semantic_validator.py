
import re

NEGATION_WORDS = {
    "not",
    "no",
    "never",
    "cannot",
    "can't",
    "don't",
    "doesn't",
    "won't",
    "shouldn't",
    "couldn't",
    "wouldn't",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
    "didn't",
    "hasn't",
    "haven't",
    "hadn't"
}


def extract_negation_words(text):
    words = re.findall(r"\b[\w']+\b", text.lower())

    return {
        word for word in words
        if word in NEGATION_WORDS
    }


def preserves_negation(original_text, candidate_text):
    original_negations = extract_negation_words(original_text)
    candidate_negations = extract_negation_words(candidate_text)

    return original_negations.issubset(candidate_negations)
