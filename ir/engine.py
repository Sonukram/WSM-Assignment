"""Facade wiring the modules together; the GUI only talks to this."""
from dataclasses import dataclass
from typing import List

from .document_loader import Document, load_documents
from .inverted_index import InvertedIndex
from .query_processor import QueryProcessor
from .wildcard import PermutermIndex


@dataclass(frozen=True)
class SearchResult:
    name: str
    snippet: str


class SearchEngine:
    def __init__(self, docs_dir: str) -> None:
        self.documents: List[Document] = load_documents(docs_dir)
        self.index = InvertedIndex.build(self.documents)
        self.wildcards = PermutermIndex(self.index.vocabulary)
        self.processor = QueryProcessor(self.index, self.wildcards)

    def search(self, query: str) -> List[SearchResult]:
        doc_ids = self.processor.search(query)
        return [
            SearchResult(self.documents[i].name, self._snippet(self.documents[i].text))
            for i in doc_ids
        ]

    @staticmethod
    def _snippet(text: str, length: int = 80) -> str:
        flat = " ".join(text.split())
        return flat if len(flat) <= length else flat[:length].rstrip() + "..."
