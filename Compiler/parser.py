# 🕊️ SAHADIA LANGUAGE
# Parser
# Official Implementation v1.1
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
    UseNode,
    FunctionNode,
    ReturnNode,
    NumberNode,
    StringNode,
    IdentifierNode,
    BinaryExpressionNode,
    FunctionCallNode
)


class SahadiaParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    def match(self, token_type, value=None):
        token = self.current()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        if value and token.value != value:
            self.error(f"Expected '{value}', got '{token.value}'")
        return self.advance()

    def error(self, message):
        token = self.current()
        raise SyntaxError(f"[Line {token.line}] {message}")

    # ============
    # ENTRY POINT
    # ============

    def parse(self):
        statements = []
        while self.current().type != "EOF":
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    # ============
    # STATEMENTS
    # ============

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
        if token.value == "Return":
            return self.parse_return()

        self.error(f"Unknown statement '{token.value}'")

    def parse_soul(self):
        self.match("KEYWORD", "Soul")
        return SoulNode(self.parse_expression())

    def parse_say(self):
        self.match("KEYWORD", "Say")
        return SayNode(self.parse_expression())

    def parse_remember(self):
        self.match("KEYWORD", "Remember")
        name = self.match("IDENTIFIER").value
        self.match("KEYWORD", "as")
        return RememberNode(name, self.parse_expression())

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

        while self.current().value not in ("ElseSoul", "EndIf"):
            then_body.append(self.parse_statement())

        else_body = None
        if self.current().value == "ElseSoul":
            self.advance()
            else_body = []
            while self.current().value != "EndIf":
                else_body.append(self.parse_statement())

        self.match("KEYWORD", "EndIf")
        return IfNode(condition, then_body, else_body)

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

    def parse_return(self):
        self.match("KEYWORD", "Return")
        return ReturnNode(self.parse_expression())

    # ============
    # EXPRESSIONS
    # ============

    def parse_expression(self):
        left = self.parse_term()
        while self.current().type in ("OPERATOR", "COMPARATOR"):
            op = self.advance().value
            right = self.parse_term()
            left = BinaryExpressionNode(left, op, right)
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
            name = self.advance().value
            if self.current().value == "of":
                self.advance()
                return FunctionCallNode(name, [self.parse_term()])
            return IdentifierNode(name)

        self.error(f"Unexpected token '{token.value}'")
