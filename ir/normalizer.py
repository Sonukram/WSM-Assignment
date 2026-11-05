"""Module 3 - Text normalization / case folding.

Applied identically to document tokens (index time) and query terms
(search time) so that they always match.
"""
import unicodedata
from typing import Iterable, List


def normalize(token: str) -> str:
    """Case-fold and strip diacritics: 'Café' -> 'cafe', 'Straße' -> 'strasse'."""
    folded = unicodedata.normalize("NFKD", token.casefold())
    return "".join(ch for ch in folded if not unicodedata.combining(ch))


def normalize_all(tokens: Iterable[str]) -> List[str]:
    return [normalize(t) for t in tokens]
