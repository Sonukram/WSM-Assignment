# ir_search

Boolean + wildcard search over a folder of `.txt` files.

```
ir_search/
├── main.py                  # entry point (launches GUI)
├── data/docs/               # sample corpus
├── tests/test_search.py     # python -m unittest discover tests
└── ir/
    ├── document_loader.py   # 1. load files -> Document
    ├── tokenizer.py         # 2. text -> tokens
    ├── normalizer.py        # 3. case folding + accent stripping
    ├── inverted_index.py    # 4. term -> sorted postings
    ├── query_processor.py   # 5. AND / OR / NOT / ( ) parser + evaluator
    ├── wildcard.py          # 6. permuterm index for '*'
    ├── gui.py               # 7. Tkinter front end
    └── engine.py            # glue between modules and GUI
```

Run: `python main.py` (or `python main.py --docs path/to/txts`).

Query examples: `quick lazy`, `fox OR cat`, `quick AND NOT dog`, `(fox OR cat) AND lazy`, `mon*`, `*key`, `m*n*y`.
Operators must be UPPERCASE. Only Python's standard library is required.
