def calculate_input_cost(token_count, price_per_million):

    if token_count < 0:
        raise ValueError("Token count cannot be negative")

    if price_per_million < 0:
        raise ValueError("Price cannot be negative")

    cost = (token_count/1_000_000) * price_per_million
    return round(cost, 10)