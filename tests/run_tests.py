"""tests/run_tests.py

Simple test runner that tokenizes every file in `sample_inputs/` and prints the
resulting token stream.

This is intended as a quick smoke test / demo harness rather than a unit-test
suite.
"""

from __future__ import annotations
import os
import sys

# Ensure repository root is on sys.path when running as a script.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer


def run_on_file(path: str) -> None:
    """Read `path`, run the lexer, and print tokens to stdout."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    lexer = Lexer(text)
    toks = lexer.tokenize()
    print("=" * 80)
    print("FILE:", os.path.basename(path))
    for t in toks:
        print(f"{t.line}:{t.col}\t{t.type:<10}\t{t.lexeme!r}")


def main():
    """Run the lexer over all sample inputs."""
    base = os.path.join(os.path.dirname(__file__), "..", "sample_inputs")
    for name in sorted(os.listdir(base)):
        if name.endswith(".py") or name.endswith(".txt"):
            run_on_file(os.path.join(base, name))


if __name__ == "__main__":
    main()
