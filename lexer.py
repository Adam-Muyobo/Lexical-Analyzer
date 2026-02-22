"""lexer.py

Implements a small Python-focused lexical analyzer for CSI428.

The lexer scans an input string character-by-character and emits a stream of
`Token` objects (type, lexeme, line, column). It supports identifiers/keywords,
numbers, strings, operators, delimiters, comments, newlines, EOF, and ERROR.

Note: Although `fa_tables.py` defines DFA states/transitions, this lexer uses a
direct (hand-coded) scan loop while reusing the same character-class function.
"""

from __future__ import annotations

import argparse
from typing import List

from keywords import PYTHON_KEYWORDS
from tokens import (
    Token,
    KEYWORD,
    IDENTIFIER,
    INTEGER,
    FLOAT,
    STRING,
    OPERATOR,
    DELIMITER,
    COMMENT,
    NEWLINE,
    EOF,
    ERROR,
)
from fa_tables import (
    S_START,
    S_IDENT,
    S_INT,
    S_FLOAT_DOT,
    S_FLOAT,
    S_STRING_SQ,
    S_STRING_DQ,
    S_COMMENT,
    S_DONE,
    char_class,
    C_NL,
    C_WS,
    C_LETTER,
    C_DIGIT,
    C_DOT,
    C_HASH,
    C_SQUOTE,
    C_DQUOTE,
    C_BSLASH,
    C_OTHER,
)

DELIMITERS = {"(", ")", "[", "]", "{", "}", ",", ":", ".", ";"}

OPERATORS = [
    "**=",
    "//=",
    "==",
    "!=",
    "<=",
    ">=",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "**",
    "//",
    "+",
    "-",
    "*",
    "/",
    "%",
    "=",
    "<",
    ">",
]


def is_operator_prefix(s: str) -> bool:
    """Return True if `s` could be the start of any supported operator.

    Used to implement maximal-munch operator matching (keep extending while the
    current slice is still a valid operator prefix).
    """
    return any(op.startswith(s) for op in OPERATORS)


def classify_ident(lexeme: str) -> str:
    """Classify an identifier lexeme as KEYWORD or IDENTIFIER."""
    return KEYWORD if lexeme in PYTHON_KEYWORDS else IDENTIFIER


class Lexer:
    def __init__(self, text: str):
        """Create a lexer over `text`.

        Tracks the current index (`i`) and current 1-based line/column for token
        source locations.
        """
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

    def _peek(self) -> str:
        """Return the current character without consuming it ("" at EOF)."""
        return "" if self.i >= len(self.text) else self.text[self.i]

    def _advance(self) -> str:
        """Consume and return the current character, updating line/column."""
        ch = self._peek()
        if ch == "":
            return ""
        self.i += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _make_token(
        self, ttype: str, lexeme: str, start_line: int, start_col: int
    ) -> Token:
        """Create a `Token` with the provided starting position."""
        return Token(ttype, lexeme, start_line, start_col)

    def tokenize(
        self, emit_newlines: bool = True, emit_comments: bool = True
    ) -> List[Token]:
        """Tokenize the input text into a list of `Token` objects.

        - `emit_newlines`: if False, NEWLINE tokens are skipped.
        - `emit_comments`: if False, COMMENT tokens are skipped.

        Always appends a final EOF token.
        """
        tokens: List[Token] = []

        while True:
            ch = self._peek()
            if ch == "":
                break

            start_line, start_col = self.line, self.col
            cc = char_class(ch)

            # Newlines
            if cc == C_NL:
                self._advance()
                if emit_newlines:
                    tokens.append(
                        self._make_token(NEWLINE, "\n", start_line, start_col)
                    )
                continue

            # Whitespace
            if cc == C_WS:
                self._advance()
                continue

            # Comments (# ...)
            if cc == C_HASH:
                lex = ""
                while True:
                    ch2 = self._peek()
                    if ch2 == "" or char_class(ch2) == C_NL:
                        break
                    lex += self._advance()
                if emit_comments:
                    tokens.append(self._make_token(COMMENT, lex, start_line, start_col))
                continue

            # Strings ('...' or "...") with escapes
            if cc in (C_SQUOTE, C_DQUOTE):
                quote = self._advance()
                lex = quote
                escaped = False
                while True:
                    ch2 = self._peek()
                    if ch2 == "":
                        tokens.append(
                            self._make_token(ERROR, lex, start_line, start_col)
                        )
                        break
                    c2 = self._advance()
                    lex += c2
                    if escaped:
                        escaped = False
                        continue
                    if c2 == "\\":
                        escaped = True
                        continue
                    if (quote == "'" and c2 == "'") or (quote == '"' and c2 == '"'):
                        tokens.append(
                            self._make_token(STRING, lex, start_line, start_col)
                        )
                        break
                    if c2 == "\n":
                        tokens.append(
                            self._make_token(ERROR, lex, start_line, start_col)
                        )
                        break
                continue

            # Identifiers / keywords
            if cc == C_LETTER:
                lex = ""
                while True:
                    ch2 = self._peek()
                    if ch2 == "":
                        break
                    c2 = char_class(ch2)
                    if c2 in (C_LETTER, C_DIGIT):
                        lex += self._advance()
                    else:
                        break
                tokens.append(
                    self._make_token(classify_ident(lex), lex, start_line, start_col)
                )
                continue

            # Numbers: int/float, including .5
            if cc == C_DIGIT or (
                cc == C_DOT
                and self.i + 1 < len(self.text)
                and char_class(self.text[self.i + 1]) == C_DIGIT
            ):
                lex = ""
                seen_dot = False
                if cc == C_DOT:
                    seen_dot = True
                    lex += self._advance()
                while True:
                    ch2 = self._peek()
                    if ch2 == "":
                        break
                    c2 = char_class(ch2)
                    if c2 == C_DIGIT:
                        lex += self._advance()
                        continue
                    if c2 == C_DOT and not seen_dot:
                        seen_dot = True
                        lex += self._advance()
                        continue
                    break
                tokens.append(
                    self._make_token(
                        FLOAT if seen_dot else INTEGER, lex, start_line, start_col
                    )
                )
                continue

            # Operators (maximal munch)
            op_lex = ""
            j = self.i
            while j < len(self.text):
                cand = self.text[self.i : j + 1]
                if is_operator_prefix(cand):
                    op_lex = cand
                    j += 1
                else:
                    break
            if op_lex in OPERATORS:
                for _ in range(len(op_lex)):
                    self._advance()
                tokens.append(self._make_token(OPERATOR, op_lex, start_line, start_col))
                continue

            # Delimiters
            if ch in DELIMITERS:
                self._advance()
                tokens.append(self._make_token(DELIMITER, ch, start_line, start_col))
                continue

            # Unknown
            self._advance()
            tokens.append(self._make_token(ERROR, ch, start_line, start_col))

        tokens.append(self._make_token(EOF, "", self.line, self.col))
        return tokens


def main():
    """CLI entrypoint: tokenize a file and print the token stream."""
    ap = argparse.ArgumentParser(
        description="CSI428 Table-Driven Python Lexical Analyzer"
    )
    ap.add_argument("path", help="Path to a file to tokenize")
    ap.add_argument("--no-newlines", action="store_true")
    ap.add_argument("--no-comments", action="store_true")
    args = ap.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        text = f.read()

    lexer = Lexer(text)
    toks = lexer.tokenize(
        emit_newlines=not args.no_newlines, emit_comments=not args.no_comments
    )
    for t in toks:
        print(f"{t.line}:{t.col}\t{t.type:<10}\t{t.lexeme!r}")


if __name__ == "__main__":
    main()
