"""Module 6 - Wildcard processing.

Permuterm index: every vocabulary term t is stored under all rotations of
t + '$'. A pattern such as  X*Y  becomes the prefix lookup  Y$X ; patterns
with several '*' are looked up by the part before the first '*' after
rotation, then verified with a regex.
"""
import re
from bisect import bisect_left
from typing import Iterable, List, Tuple

from .normalizer import normalize


class PermutermIndex:
    def __init__(self, vocabulary: Iterable[str]) -> None:
        rotations: List[Tuple[str, str]] = []
        for term in vocabulary:
            t = term + "$"
            rotations.extend((t[i:] + t[:i], term) for i in range(len(t)))
        rotations.sort()
        self._rotations = rotations

    @staticmethod
    def is_wildcard(word: str) -> bool:
        return "*" in word

    def expand(self, pattern: str) -> List[str]:
        """Return all vocabulary terms matching `pattern` ('*' = any chars)."""
        pattern = re.sub(r"\*+", "*", normalize(pattern))
        if pattern == "*":
            return sorted({term for _, term in self._rotations})

        p = pattern + "$"
        last_star = p.rfind("*")
        rotated = p[last_star + 1:] + p[: last_star + 1]   # e.g. Z$X*Y*
        prefix = rotated.split("*", 1)[0]                  # e.g. Z$X

        regex = re.compile(".*".join(re.escape(part) for part in pattern.split("*")))

        start = bisect_left(self._rotations, (prefix,))
        matches = set()
        for rotation, term in self._rotations[start:]:
            if not rotation.startswith(prefix):
                break
            if regex.fullmatch(term):
                matches.add(term)
        return sorted(matches)
