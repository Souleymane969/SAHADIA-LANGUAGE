# 🕊️ SAHADIA LANGUAGE
# Parser
# Official Implementation v1.0
#
# In memory of Sahadia.

from typing import List
from compiler.lexer import Token
from compiler.ast import (
    ProgramNode,
    SoulNode,
    SayNode,
    RememberNode,
    AskNode,
    IfNode,
    RepeatNode,
    NumberNode,
    StringNode,
    IdentifierNode,
    BinaryExpressionNode,
    UseNode,
    FunctionNode,
    ReturnNode
)


# =========================
# PARSER
# =========================

class SahadiaParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    # -------------------------
    # HELPERS
    # -------------------------
    def current(self) -> Token:
        return self.tokens[self.position]

    def advance(self) -> Token:
        token = self.current()
        self.position += 1
        return token

    def match(self, token_type: str, value: str = None) -> Token:
        token = self.current()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        if value and token.value != value:
            self.error(f"Expected '{value}', got '{token.value}'")
        return self.advance()

    def error(self, message: str):
        token = self.current()
        raise SyntaxError(f"[Line {token.line}] {message}")

    # -------------------------
    # ENTRY POINT
    # -------------------------
    def parse(self) -> ProgramNode:
        statements = []

        while self.current().type != "EOF":
            statements.append(self.parse_statement())

        return ProgramNode(statements)

    # -------------------------
    # STATEMENTS
    # -------------------------
    def parse_statement(self):
        token = self.current()

        if token.value == "Soul":
            return self.parse_soul()

        if token.value == "Say":
            return self.parse_say()

        if token.value == "Remember":
            return self.parse_remember()

        if token.value == "Ask":
            return self.parse_ask()

        if token.value == "IfSoul":
            return self.parse_if()

        if token.value == "RepeatSoul":
            return self.parse_repeat()

        if token.value == "Use":
            return self.parse_use()

        if token.value == "Function":
            return self.parse_function()

        if token.value == "Return":
            return self.parse_return()

        self.error(f"Unknown statement '{token.value}'")

    # -------------------------
    # INDIVIDUAL STATEMENTS
    # -------------------------
    def parse_soul(self):
        self.match("KEYWORD", "Soul")
        message = self.parse_expression()
        return SoulNode(message)

    def parse_say(self):
        self.match("KEYWORD", "Say")
        message = self.parse_expression()
        return SayNode(message)

    def parse_remember(self):
        self.match("KEYWORD", "Remember")
        name = self.match("IDENTIFIER").value
        self.match("KEYWORD", "as")
        value = self.parse_expression()
        return RememberNode(name, value)

    def parse_ask(self):
        self.match("KEYWORD", "Ask")
        question = self.parse_expression()
        self.match("KEYWORD", "into")
        target = self.match("IDENTIFIER").value
        return AskNode(question, target)

    def parse_if(self):
        self.match("KEYWORD", "IfSoul")
        condition = self.parse_expression()

        then_body = []
        else_body = []

        while self.current().value not in ("ElseSoul", "EndIf"):
            then_body.append(self.parse_statement())

        if self.current().value == "ElseSoul":
            self.advance()
            while self.current().value != "EndIf":
                else_body.append(self.parse_statement())

        self.match("KEYWORD", "EndIf")
        return IfNode(condition, then_body, else_body or None)

    def parse_repeat(self):
        self.match("KEYWORD", "RepeatSoul")
        times = self.parse_expression()
        self.match("KEYWORD", "times")

        body = []
        while self.current().value != "EndRepeat":
            body.append(self.parse_statement())

        self.match("KEYWORD", "EndRepeat")
        return RepeatNode(times, body)

    def parse_use(self):
        self.match("KEYWORD", "Use")
        name = self.match("IDENTIFIER").value
        return UseNode(name)

    def parse_function(self):
        self.match("KEYWORD", "Function")
        name = self.match("IDENTIFIER").value
        self.match("KEYWORD", "of")

        params = [self.match("IDENTIFIER").value]

        body = []
        while self.current().value != "EndFunction":
            body.append(self.parse_statement())

        self.match("KEYWORD", "EndFunction")
        return FunctionNode(name, params, body)

    def parse_return(self):
        self.match("KEYWORD", "Return")
        value = self.parse_expression()
        return ReturnNode(value)

    # -------------------------
    # EXPRESSIONS
    # -------------------------
    def parse_expression(self):
        left = self.parse_term()

        while self.current().type in ("OPERATOR", "COMPARATOR"):
            operator = self.advance().value
            right = self.parse_term()
            left = BinaryExpressionNode(left, operator, right)

        return left

    def parse_term(self):
        token = self.current()

        if token.type == "NUMBER":
            self.advance()
            return NumberNode(float(token.value))

        if token.type == "STRING":
            self.advance()
            return StringNode(token.value)

        if token.type == "IDENTIFIER":
            self.advance()
            return IdentifierNode(token.value)

        self.error(f"Unexpected token '{token.value}' in expression")
