import re

def remove_duplicate_lines(text):
    lines = text.splitlines()

    seen = set()
    result = []

    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)

    
    return "\n".join(result)

def normalize_whitespace(text):

    text = re.sub(r"[ \t]+", " ",text)

    lines = [line.strip() for line in text.splitlines()]

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def remove_duplicate_sentences(text):
    if not text.strip():
        return ""

    sentences = re.split(
        r'(?<=[.!?])\s+|\n+',
        text.strip()
    )

    seen = set()
    unique_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        key = sentence.casefold()

        if key not in seen:
            seen.add(key)
            unique_sentences.append(sentence)

    return " ".join(unique_sentences)

def remove_repeated_phrases(text):
    if not text.strip():
        return ""

    pattern = re.compile(
        r"\b(?P<phrase>(?:[\w'-]+[ \t]+){1,}[\w'-]+)(?:[ \t]+(?P=phrase))\b",
        flags=re.IGNORECASE
    )

    return pattern.sub(r"\g<phrase>", text)