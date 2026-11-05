"""Entry point:  python main.py [--docs data/docs]"""
import argparse

from ir.engine import SearchEngine
from ir.gui import SearchApp


def main() -> None:
    parser = argparse.ArgumentParser(description="Boolean + wildcard document search")
    parser.add_argument("--docs", default="data/docs", help="directory of .txt files")
    args = parser.parse_args()

    engine = SearchEngine(args.docs)
    SearchApp(engine.search).mainloop()


if __name__ == "__main__":
    main()
