import tiktoken

def count_tokens(text):

    if not text:
        return 0
    
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


if __name__ == "__main__":
    sample = "Python is useful. Token optimization saves money."
    token_count = count_tokens(sample)
    print(f"Token count: {token_count}")