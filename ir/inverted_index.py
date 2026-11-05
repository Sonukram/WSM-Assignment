"""Module 4 - Inverted index construction.

term -> sorted list of doc ids containing that term.
"""
from typing import Dict, Iterable, List

from .document_loader import Document
from .normalizer import normalize_all
from .tokenizer import tokenize


class InvertedIndex:
    def __init__(self) -> None:
        self._postings: Dict[str, List[int]] = {}
        self._doc_ids: List[int] = []

    @classmethod
    def build(cls, documents: Iterable[Document]) -> "InvertedIndex":
        index = cls()
        for doc in documents:  # docs arrive in ascending doc_id order
            index._doc_ids.append(doc.doc_id)
            for term in set(normalize_all(tokenize(doc.text))):
                index._postings.setdefault(term, []).append(doc.doc_id)
        return index

    def postings(self, term: str) -> List[int]:
        return self._postings.get(term, [])

    @property
    def vocabulary(self) -> List[str]:
        return sorted(self._postings)

    @property
    def all_doc_ids(self) -> List[int]:
        return self._doc_ids
