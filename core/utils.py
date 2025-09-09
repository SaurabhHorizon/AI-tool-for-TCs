import re
from typing import List

def clean_text(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "")).strip()

def chunk_text(text: str, max_words: int = 120) -> List[str]:
    """Split long text into roughly-equal chunks by sentence/word count."""
    text = clean_text(text)
    if not text:
        return []
    parts, acc = [], []
    for word in text.split():
        acc.append(word)
        if len(acc) >= max_words:
            parts.append(" ".join(acc))
            acc = []
    if acc:
        parts.append(" ".join(acc))
    return parts

def slugify(s: str) -> str:
    s = clean_text(s).lower()
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s[:60]
