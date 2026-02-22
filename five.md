# Explain Like I'm 5 (But For Devs)

This project is a tiny "word splitter" for Python code.
It reads a Python file and breaks it into little pieces called *tokens* (like
"def", "add", "(", "3.14", or "# a comment").

Below is what each file does, explained super simply.

## `lexer.py`
This is the main "token maker".

- It looks at the input text one character at a time.
- It groups characters into meaningful chunks:
  - names like `total`
  - numbers like `10` or `3.14`
  - strings like `"Hello"`
  - operators like `+` or `>=`
  - delimiters like `(` `)` `{` `}` `,` `:`
  - comments that start with `#`
- It remembers where each token starts (line and column), like pointing to a
  spot in a book.

It also has a small command-line mode so you can run it on a file and print the
tokens.

## `tokens.py`
This file defines what a token looks like.

- A `Token` is a little "label" that stores:
  - what kind of thing it is (type)
  - the actual text (lexeme)
  - where it came from (line and column)
- It also lists all the token type names (like `KEYWORD`, `INTEGER`, `EOF`).

So `lexer.py` can create tokens in a consistent way.

## `keywords.py`
This is just a list (a set) of Python's special reserved words.

- Words like `def`, `class`, `return`, `if`, `else`, etc.

When the lexer sees a name, it checks this set to decide:
- "Is this a KEYWORD?" or
- "Is this a normal IDENTIFIER?"

## `fa_tables.py`
This file is the "rule book" for a DFA-style lexer.

- It defines state numbers (like `S_START`, `S_IDENT`).
- It defines character groups (like LETTER, DIGIT, DOT, NEWLINE).
- `char_class()` tells you which group a character belongs to.
- `transitions` is a table that says:
  "If I'm in state X and I see character-class Y, go to state Z."

In this project, `lexer.py` mostly uses `char_class()` directly during scanning,
and the transition table is there as the formal FA representation for the
assignment/report.

## `tests/run_tests.py`
This is a simple "try it on everything" script.

- It looks inside `sample_inputs/`.
- For each sample file, it runs the lexer.
- It prints all the tokens so you can eyeball the output.

It's more of a demo/smoke test than a strict unit test.

## `README.md`
This is the "how to use it" page.

- It tells you what the project is.
- It lists the files.
- It shows how to run the lexer and the test script.
- It describes the token types the lexer can produce.

## `sample_inputs/`
These are tiny example programs.

- They exist so you can run the lexer and see if it behaves correctly.

## `tests/`
This folder holds test/demo scripts.

- Right now it contains the runner that prints token output for the samples.
