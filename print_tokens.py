from collections import defaultdict
import re

def tokenize(file_name: str) -> list:
    toks = []
    try:
        with open(file_name, "r") as f:
            for line in f:
                strings = re.split('[^a-zA-Z0-9]', line)
                for string in strings:
                    if string != "":
                        toks.append(string.lower())
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    return toks

def compute_word_frequencies(tokens: list) -> dict:
    word_freqs = defaultdict(int)
    for tok in tokens:
        word_freqs[tok] += 1
    return word_freqs

def print_top_50_frequencies(tok_freqs: dict) -> None:
    for i, assoc in enumerate(sorted(tok_freqs, key=tok_freqs.get, reverse=True)[:50]):
        print(f"{i}:\t{assoc}\t{tok_freqs[assoc]}")


if __name__ == "__main__":
    file_name = "bin/tokens.txt"
    tokens = tokenize(file_name)
    word_freqs = compute_word_frequencies(tokens)
    print_top_50_frequencies(word_freqs)