# CSI428 Lexical Analyzer (Question 1)

Table-driven lexical analyzer for **Python** built for **CSI428 – Programming Language Translation** (Assignment I, Q1).  
The lexer reads input **character-by-character** and uses a **DFA transition table (FA table)** for core token families.

## Files
- `lexer.py` – lexer implementation + CLI (prints token stream)
- `fa_tables.py` – DFA states, character classes, transition table
- `tokens.py` – `Token` dataclass + token type constants
- `keywords.py` – Python keyword set
- `sample_inputs/` – sample programs for testing
- `tests/run_tests.py` – run lexer across all sample inputs

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

## Notes for Report
Explain:
1) token list + descriptions  
2) FA: character classes, states, transitions  
3) implementation: char-by-char scanning + maximal munch  
4) testing: sample inputs and outputs

## Authors
Tida, Zibisani, Adam
