from token_counter import count_tokens
from candidate_engine import select_best_candidate
from cost_calculator import calculate_input_cost
from pricing import MODEL_PRICING


def optimize_text(text, model_name="SampleLLM"):

    # Validate model
    if model_name not in MODEL_PRICING:
        raise ValueError(f"Unknown model: {model_name}")

    # Count original tokens
    original_count = count_tokens(text)

    # Run the candidate comparison engine
    candidate_result = select_best_candidate(text)

    optimized_text = candidate_result["optimized_text"]
    optimized_count = candidate_result["optimized_token_count"]
    strategy_results = candidate_result["strategy_results"]

    selected_strategy = candidate_result["selected_strategy"]

# Safety check: never accept a candidate with more tokens
    if optimized_count > original_count:
        optimized_text = text
        optimized_count = original_count
        selected_strategy = "original"

    # Calculate tokens saved
    tokens_saved = original_count - optimized_count

    # Calculate savings percentage
    if original_count > 0:
        savings_percentage = (tokens_saved / original_count) * 100
    else:
        savings_percentage = 0

    # Determine optimization status
    optimization_applied = optimized_count < original_count

    if optimization_applied:
        optimization_status = "improved"
    else:
        optimization_status = "unchanged"

    # Calculate costs
    price = MODEL_PRICING[model_name]["input_price_per_million"]

    original_cost = calculate_input_cost(original_count, price)
    optimized_cost = calculate_input_cost(optimized_count, price)

    estimated_cost_saved = original_cost - optimized_cost

    return {
        "original_text": text,
        "optimized_text": optimized_text,
        "original_token_count": original_count,
        "optimized_token_count": optimized_count,
        "tokens_saved": tokens_saved,
        "savings_Percentage": round(savings_percentage, 2),
        "original_input_cost": original_cost,
        "optimized_input_cost": optimized_cost,
        "estimated_cost_saved": round(estimated_cost_saved, 10),
        "model_name": model_name,
        "optimization_applied": optimization_applied,
        "optimization_status": optimization_status,
        "selected_strategy": selected_strategy,
        "strategy_results": strategy_results
    }