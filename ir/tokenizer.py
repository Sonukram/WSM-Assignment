"""Module 2 - Tokenization.

Splits raw text into word tokens (runs of letters/digits). No case folding
happens here; that is the normalizer's job.
"""
import re
from typing import List

# [^\W_]+ = one or more Unicode letters/digits (underscore excluded)
_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


def tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text)
