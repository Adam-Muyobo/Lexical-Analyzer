"""tokens.py

Defines the `Token` data structure and the set of token-type string constants
used by the lexer.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    """A single lexical token produced by the lexer.

    `line` and `col` are 1-based positions of the first character of `lexeme`.
    """

    type: str
    lexeme: str
    line: int
    col: int


# Token type names (kept as strings for easy printing/formatting).
KEYWORD = "KEYWORD"
IDENTIFIER = "IDENTIFIER"
INTEGER = "INTEGER"
FLOAT = "FLOAT"
STRING = "STRING"
OPERATOR = "OPERATOR"
DELIMITER = "DELIMITER"
COMMENT = "COMMENT"
NEWLINE = "NEWLINE"
EOF = "EOF"
ERROR = "ERROR"
