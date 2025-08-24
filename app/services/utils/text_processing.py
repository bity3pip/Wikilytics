import re
from typing import List
import tiktoken

MODEL_NAME = "gpt-4o-mini"


def tokenize_text(text: str) -> List[int]:
    enc = tiktoken.encoding_for_model(MODEL_NAME)
    return enc.encode(text)


def detokenize_tokens(tokens: List[int]) -> str:
    enc = tiktoken.encoding_for_model(MODEL_NAME)
    return enc.decode(tokens)


def chunk_text_by_tokens(
        text: str,
        max_tokens: int = 500,
        overlap_tokens: int = 50
) -> List[str]:

    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk_tokens = []

    for sentence in sentences:
        sentence_tokens = tokenize_text(sentence)
        if len(current_chunk_tokens) + len(sentence_tokens) <= max_tokens:
            current_chunk_tokens.extend(sentence_tokens)
        else:
            chunks.append(detokenize_tokens(current_chunk_tokens))
            overlap = current_chunk_tokens[-overlap_tokens:] \
                if overlap_tokens < len(current_chunk_tokens) \
                else current_chunk_tokens
            current_chunk_tokens = overlap + sentence_tokens

    if current_chunk_tokens:
        chunks.append(detokenize_tokens(current_chunk_tokens))

    return chunks
