"""Module 7 - Frontend GUI (Tkinter).

Search input box, Search button, and a read-only result area. The GUI knows
nothing about indexing: it receives a `search_fn(query) -> list[SearchResult]`.
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import Callable, List

from .engine import SearchResult
from .query_processor import QuerySyntaxError


class SearchApp(tk.Tk):
    def __init__(self, search_fn: Callable[[str], List[SearchResult]]) -> None:
        super().__init__()
        self.title("Document Search")
        self.geometry("640x420")
        self._search_fn = search_fn

        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")
        self.query_var = tk.StringVar()
        self.entry = ttk.Entry(top, textvariable=self.query_var)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.on_search())
        self.entry.focus_set()
        ttk.Button(top, text="Search", command=self.on_search).pack(side="left", padx=(8, 0))

        self.results = scrolledtext.ScrolledText(self, wrap="word", state="disabled")
        self.results.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def on_search(self) -> None:
        query = self.query_var.get().strip()
        if not query:
            self._show("Enter a query.")
            return
        try:
            hits = self._search_fn(query)
        except QuerySyntaxError as exc:
            self._show(f"Query error: {exc}")
            return
        if not hits:
            self._show("No documents found.")
            return
        lines = [f"{len(hits)} document(s) found:\n"]
        lines += [f"- {h.name}\n    {h.snippet}\n" for h in hits]
        self._show("\n".join(lines))

    def _show(self, text: str) -> None:
        self.results.configure(state="normal")   # temporarily writable
        self.results.delete("1.0", "end")
        self.results.insert("1.0", text)
        self.results.configure(state="disabled")  # read-only again
