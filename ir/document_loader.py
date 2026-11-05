"""Module 1 - Document loading.

Reads plain-text files from a directory and assigns each one an integer doc id.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Document:
    doc_id: int
    name: str
    path: Path
    text: str


def load_documents(directory: str, extensions=(".txt",)) -> List[Document]:
    """Load every file in `directory` whose suffix is in `extensions`.

    Doc ids are assigned in sorted-filename order starting at 0, so postings
    lists built in that order are automatically sorted.
    """
    root = Path(directory)
    if not root.is_dir():
        raise FileNotFoundError(f"Document directory not found: {root}")

    docs: List[Document] = []
    paths = sorted(p for p in root.iterdir() if p.suffix.lower() in extensions)
    for doc_id, path in enumerate(paths):
        text = path.read_text(encoding="utf-8", errors="replace")
        docs.append(Document(doc_id, path.name, path, text))
    return docs
