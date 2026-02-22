# Lexical Analyzer

Table-driven lexical analyzer for **Python** built for **CSI428 – Programming Language Translation** (Assignment I, Q1, 2025/2026 Semester 2).  
The lexer reads input **character-by-character** and uses a **DFA transition table (FA table)** for core token families.

## Files
- `lexer.py` – lexer implementation + CLI (prints token stream)
- `fa_tables.py` – DFA states, character classes, transition table
- `tokens.py` – `Token` dataclass + token type constants
- `keywords.py` – Python keyword set
- `sample_inputs/` – sample programs for testing
- `tests/run_tests.py` – run lexer across all sample inputs
#### When in doubt just read five.md

## Token Types Supported
- `KEYWORD`, `IDENTIFIER`
- `INTEGER`, `FLOAT`
- `STRING` (single/double quotes; supports escapes)
- `OPERATOR` (maximal munch): `+ - * / // % ** = == != < <= > >= += -= *= /= %=`
- `DELIMITER`: `()[]{} , : . ;`
- `COMMENT` (`# ...`)
- `NEWLINE`, `EOF`, `ERROR`

> INDENT/DEDENT not required for Q1, so they are not emitted.

## Usage

Tokenize a file:
```bash
python lexer.py sample_inputs/sample1.py
```

Run tests on all samples:
```bash
python tests/run_tests.py
```

Options:
- `--no-newlines` : do not emit `NEWLINE`
- `--no-comments` : do not emit `COMMENT`

## Output Format
Each token prints as:
```
line:col    TOKEN_TYPE    'lexeme'
```

## Authors
- Adam Musakabantu Muyobo
- Zibisani Kgari Mholo
- Theo Kizito Tida
