from semantic_validator import validate_semantics
from token_counter import count_tokens
from optimizer import (
    remove_duplicate_lines,
    normalize_whitespace,
    remove_duplicate_sentences,
    remove_repeated_phrases,
    shorten_common_expressions,
    remove_filler_words
)



def select_best_candidate(original_text):

    original_count = count_tokens(original_text)

    candidates = [
        {
            "strategy": "original",
            "text": original_text
        },
        {
            "strategy": "duplicate_line_removal",
            "text": remove_duplicate_lines(original_text)
        },
        {
            "strategy": "whitespace_normalization",
            "text": normalize_whitespace(original_text)
        },
        {
            "strategy": "duplicate_sentence_removal",
            "text": remove_duplicate_sentences(original_text)
        },
        {
            "strategy": "repeated_phrase_removal",
            "text": remove_repeated_phrases(original_text)
        },
        {
            "strategy": "common_expression_shortening",
            "text": shorten_common_expressions(original_text)
        },
        {
            "strategy": "filler_word_removal",
            "text": remove_filler_words(original_text)
        }   
    ]

    best_candidate = candidates[0]
    best_token_count = original_count

    strategy_results = []

    for candidate in candidates:

        current_token_count = count_tokens(candidate["text"])

        tokens_saved = original_count - current_token_count

        validation_result = validate_semantics(
            original_text,
            candidate["text"]
        )

        is_semantically_safe = validation_result["is_safe"]

        if is_semantically_safe and current_token_count < best_token_count:
            best_candidate = candidate
            best_token_count = current_token_count

        strategy_results.append({
            "strategy": candidate["strategy"],
            "token_count": current_token_count,
            "tokens_saved": tokens_saved,
            "savings_percentage": round(
                (tokens_saved / original_count) * 100, 2
            ) if original_count > 0 else 0
        })

    return {
        "optimized_text": best_candidate["text"],
        "selected_strategy": best_candidate["strategy"],
        "optimized_token_count": best_token_count,
        "strategy_results": strategy_results
    }
