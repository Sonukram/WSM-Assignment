"""Module 5 - Query processing.

Grammar (operators must be UPPERCASE; adjacent terms mean AND):

    expr   := and_expr ( OR and_expr )*
    and_expr := not_expr ( [AND] not_expr )*
    not_expr := NOT not_expr | atom
    atom   := '(' expr ')' | word

Words containing '*' are expanded through the permuterm index.
"""
import re
from typing import List

from .inverted_index import InvertedIndex
from .normalizer import normalize_all
from .tokenizer import tokenize
from .wildcard import PermutermIndex

_LEX_RE = re.compile(r"\(|\)|[^\s()]+")
_OPERATORS = {"AND", "OR", "NOT"}


class QuerySyntaxError(ValueError):
    pass


# ---- sorted-postings set operations -------------------------------------
def intersect(a: List[int], b: List[int]) -> List[int]:
    i = j = 0
    out: List[int] = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out


def union(a: List[int], b: List[int]) -> List[int]:
    i = j = 0
    out: List[int] = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out


def difference(a: List[int], b: List[int]) -> List[int]:
    drop = set(b)
    return [x for x in a if x not in drop]


# ---- processor -----------------------------------------------------------
class QueryProcessor:
    def __init__(self, index: InvertedIndex, wildcard_index: PermutermIndex) -> None:
        self._index = index
        self._wild = wildcard_index
        self._tokens: List[str] = []
        self._pos = 0

    def search(self, query: str) -> List[int]:
        self._tokens = _LEX_RE.findall(query)
        self._pos = 0
        if not self._tokens:
            return []
        result = self._parse_or()
        if self._pos != len(self._tokens):
            raise QuerySyntaxError(f"Unexpected '{self._tokens[self._pos]}'")
        return result

    # -- parser helpers
    def _peek(self):
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _next(self):
        tok = self._peek()
        self._pos += 1
        return tok

    def _parse_or(self) -> List[int]:
        result = self._parse_and()
        while self._peek() == "OR":
            self._next()
            result = union(result, self._parse_and())
        return result

    def _parse_and(self) -> List[int]:
        result = self._parse_not()
        while self._peek() not in (None, "OR", ")"):
            if self._peek() == "AND":
                self._next()
            result = intersect(result, self._parse_not())
        return result

    def _parse_not(self) -> List[int]:
        if self._peek() == "NOT":
            self._next()
            return difference(self._index.all_doc_ids, self._parse_not())
        return self._parse_atom()

    def _parse_atom(self) -> List[int]:
        tok = self._next()
        if tok is None:
            raise QuerySyntaxError("Query ended unexpectedly")
        if tok == "(":
            result = self._parse_or()
            if self._next() != ")":
                raise QuerySyntaxError("Missing closing ')'")
            return result
        if tok == ")" or tok in _OPERATORS:
            raise QuerySyntaxError(f"Unexpected '{tok}'")
        return self._term_postings(tok)

    # -- term evaluation
    def _term_postings(self, word: str) -> List[int]:
        if PermutermIndex.is_wildcard(word):
            result: List[int] = []
            for term in self._wild.expand(word):
                result = union(result, self._index.postings(term))
            return result

        terms = normalize_all(tokenize(word))   # 'well-known' -> two terms, ANDed
        if not terms:
            return []
        result = self._index.postings(terms[0])
        for term in terms[1:]:
            result = intersect(result, self._index.postings(term))
        return result
