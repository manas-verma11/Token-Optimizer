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

def shorten_common_expressions(text):
    if not text.strip():
        return ""

    replacements = {
        "due to the fact that": "because",
        "at this point in time": "now",
        "at the present time": "now",
        "in the near future": "soon",
        "in the event that": "if",
        "despite the fact that": "although",
        "for the reason that": "because",
        "on a daily basis": "daily",
        "on a regular basis": "regularly",
        "in order to": "to",
        "make use of": "use",
        "for the purpose of": "for"
    }

    for original, replacement in replacements.items():
        pattern = re.compile(
            r"\b" + re.escape(original) + r"\b",
            flags=re.IGNORECASE
        )

        def replace_match(match):
            original_text = match.group(0)

            if original_text.isupper():
                return replacement.upper()

            if original_text[0].isupper():
                return replacement.capitalize()

            return replacement

        text = pattern.sub(replace_match, text)

    return text