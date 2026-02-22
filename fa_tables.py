"""fa_tables.py

Defines the DFA-style building blocks used by the lexical analyzer:

- State IDs (S_*) for token families like identifiers, numbers, strings, and
  comments.
- Character-class labels (C_*) to reduce the input alphabet.
- `char_class()` to map a raw character to its character class.
- `transitions`: a table mapping (state, character-class) -> next state.

In this repository, the lexer primarily uses `char_class()` during scanning,
while the `transitions` table serves as the formal FA representation for the
assignment/report.
"""

S_START = 0
S_IDENT = 1
S_INT = 2
S_FLOAT_DOT = 3
S_FLOAT = 4
S_STRING_SQ = 5
S_STRING_DQ = 6
S_COMMENT = 8
S_DONE = 9

C_WS = "WS"
C_NL = "NL"
C_LETTER = "LETTER"
C_DIGIT = "DIGIT"
C_DOT = "DOT"
C_HASH = "HASH"
C_SQUOTE = "SQUOTE"
C_DQUOTE = "DQUOTE"
C_BSLASH = "BSLASH"
C_OTHER = "OTHER"


def char_class(ch: str) -> str:
    """Map a single character to a simplified character class."""
    if ch == "":
        return C_OTHER
    if ch in (" ", "\t"):
        return C_WS
    if ch == "\n":
        return C_NL
    if ch == "_" or ("a" <= ch <= "z") or ("A" <= ch <= "Z"):
        return C_LETTER
    if "0" <= ch <= "9":
        return C_DIGIT
    if ch == ".":
        return C_DOT
    if ch == "#":
        return C_HASH
    if ch == "'":
        return C_SQUOTE
    if ch == '"':
        return C_DQUOTE
    if ch == "\\":
        return C_BSLASH
    return C_OTHER


transitions = {
    # DFA transition table: transitions[state][character_class] -> next_state
    S_START: {
        C_WS: S_START,
        C_NL: S_START,
        C_LETTER: S_IDENT,
        C_DIGIT: S_INT,
        C_DOT: S_DONE,
        C_HASH: S_COMMENT,
        C_SQUOTE: S_STRING_SQ,
        C_DQUOTE: S_STRING_DQ,
        C_OTHER: S_DONE,
    },
    S_IDENT: {
        C_LETTER: S_IDENT,
        C_DIGIT: S_IDENT,
        C_OTHER: S_DONE,
        C_WS: S_DONE,
        C_NL: S_DONE,
        C_DOT: S_DONE,
        C_HASH: S_DONE,
        C_SQUOTE: S_DONE,
        C_DQUOTE: S_DONE,
        C_BSLASH: S_DONE,
    },
    S_INT: {
        C_DIGIT: S_INT,
        C_DOT: S_FLOAT_DOT,
        C_OTHER: S_DONE,
        C_WS: S_DONE,
        C_NL: S_DONE,
        C_LETTER: S_DONE,
        C_HASH: S_DONE,
        C_SQUOTE: S_DONE,
        C_DQUOTE: S_DONE,
        C_BSLASH: S_DONE,
    },
    S_FLOAT_DOT: {
        C_DIGIT: S_FLOAT,
        C_OTHER: S_DONE,
        C_WS: S_DONE,
        C_NL: S_DONE,
        C_DOT: S_DONE,
        C_LETTER: S_DONE,
        C_HASH: S_DONE,
        C_SQUOTE: S_DONE,
        C_DQUOTE: S_DONE,
        C_BSLASH: S_DONE,
    },
    S_FLOAT: {
        C_DIGIT: S_FLOAT,
        C_OTHER: S_DONE,
        C_WS: S_DONE,
        C_NL: S_DONE,
        C_DOT: S_DONE,
        C_LETTER: S_DONE,
        C_HASH: S_DONE,
        C_SQUOTE: S_DONE,
        C_DQUOTE: S_DONE,
        C_BSLASH: S_DONE,
    },
    S_COMMENT: {
        C_NL: S_DONE,
        C_OTHER: S_COMMENT,
        C_WS: S_COMMENT,
        C_LETTER: S_COMMENT,
        C_DIGIT: S_COMMENT,
        C_DOT: S_COMMENT,
        C_HASH: S_COMMENT,
        C_SQUOTE: S_COMMENT,
        C_DQUOTE: S_COMMENT,
        C_BSLASH: S_COMMENT,
    },
}
