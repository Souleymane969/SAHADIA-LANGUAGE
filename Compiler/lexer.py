# 🕊️ SAHADIA LANGUAGE
# Lexer / Tokenizer
# Official Implementation v1.1
#
# In memory of Sahadia.

import re
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str
    line: int


KEYWORDS = {
    "Soul", "Say",
    "Remember", "as",
    "Ask", "into",
    "IfSoul", "ElseSoul", "EndIf",
    "RepeatSoul", "times", "EndRepeat",
    "Use", "Return",
    "of"
}

OPERATORS = {
    "plus", "minus", "fois", "divided", "power"
}

COMPARATORS = {
    "above", "greater",
    "below", "less",
    "equal", "same",
    "not", "different"
}


class SahadiaLexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.source):
            char = self.source[self.position]

            if char in " \t":
                self.position += 1
                continue

            if char == "\n":
                self.line += 1
                self.position += 1
                continue

            if char == '"':
                self.tokens.append(self.read_string())
                continue

            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            if char.isalpha():
                self.tokens.append(self.read_word())
                continue

            self.error(f"Unexpected character '{char}'")

        self.tokens.append(Token("EOF", "EOF", self.line))
        return self.tokens

    # ==================
    # READERS
    # ==================

    def read_string(self):
        self.position += 1
        start = self.position
        while self.position < len(self.source) and self.source[self.position] != '"':
            self.position += 1
        value = self.source[start:self.position]
        self.position += 1
        return Token("STRING", value, self.line)

    def read_number(self):
        start = self.position
        while self.position < len(self.source) and (
            self.source[self.position].isdigit() or self.source[self.position] == "."
        ):
            self.position += 1
        return Token("NUMBER", self.source[start:self.position], self.line)

    def read_word(self):
        start = self.position
        while self.position < len(self.source) and self.source[self.position].isalnum():
            self.position += 1
        value = self.source[start:self.position]

        if value in KEYWORDS:
            return Token("KEYWORD", value, self.line)
        if value in OPERATORS:
            return Token("OPERATOR", value, self.line)
        if value in COMPARATORS:
            return Token("COMPARATOR", value, self.line)

        return Token("IDENTIFIER", value, self.line)

    # ==================
    # ERROR
    # ==================

    def error(self, message):
        raise SyntaxError(f"[Line {self.line}] {message}")
