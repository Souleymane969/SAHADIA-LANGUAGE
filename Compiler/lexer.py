# 🕊️ SAHADIA LANGUAGE
# Lexer (Tokenizer)
# Official Implementation v1.0
#
# In memory of Sahadia.

import re
from dataclasses import dataclass
from typing import List


# =========================
# TOKEN DEFINITION
# =========================

@dataclass
class Token:
    type: str
    value: str
    line: int


# =========================
# LEXER
# =========================

class SahadiaLexer:
    def __init__(self, source_code: str):
        self.source = source_code.splitlines()
        self.tokens: List[Token] = []
        self.line_number = 0

    # -------------------------
    # KEYWORDS
    # -------------------------
    KEYWORDS = {
        "BeginSoul", "EndSoul",
        "Soul", "Say",
        "Remember", "as",
        "Count",
        "Ask", "into",
        "IfSoul", "ElseSoul", "EndIf",
        "RepeatSoul", "times", "EndRepeat",
        "Create", "EndCreate",
        "Build", "EndBuild",
        "WaitSoul",
        "Use",
        "Function", "of", "EndFunction",
        "Return"
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

    # -------------------------
    # MAIN ENTRY
    # -------------------------
    def tokenize(self) -> List[Token]:
        for line in self.source:
            self.line_number += 1
            self._tokenize_line(line)

        self.tokens.append(Token("EOF", "", self.line_number))
        return self.tokens

    # -------------------------
    # LINE TOKENIZATION
    # -------------------------
    def _tokenize_line(self, line: str):
        stripped = line.strip()

        # Ignore empty lines
        if not stripped:
            return

        # Ignore comments
        if stripped.startswith("#"):
            return

        # String literals
        string_matches = re.finditer(r'"([^"]*)"', line)
        strings = {}
        for i, match in enumerate(string_matches):
            placeholder = f"__STRING{i}__"
            strings[placeholder] = match.group(1)
            line = line.replace(match.group(0), placeholder)

        parts = line.strip().split()

        for part in parts:
            # Restore string
            if part in strings:
                self.tokens.append(Token("STRING", strings[part], self.line_number))
                continue

            # Keyword
            if part in self.KEYWORDS:
                self.tokens.append(Token("KEYWORD", part, self.line_number))
                continue

            # Operator
            if part in self.OPERATORS:
                self.tokens.append(Token("OPERATOR", part, self.line_number))
                continue

            # Comparator
            if part in self.COMPARATORS:
                self.tokens.append(Token("COMPARATOR", part, self.line_number))
                continue

            # Number
            if self._is_number(part):
                self.tokens.append(Token("NUMBER", part, self.line_number))
                continue

            # Identifier
            if part.isidentifier():
                self.tokens.append(Token("IDENTIFIER", part, self.line_number))
                continue

            # Unknown token
            self.tokens.append(Token("UNKNOWN", part, self.line_number))

    # -------------------------
    # HELPERS
    # -------------------------
    @staticmethod
    def _is_number(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
