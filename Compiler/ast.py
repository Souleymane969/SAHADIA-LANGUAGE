# 🕊️ SAHADIA LANGUAGE
# Abstract Syntax Tree (AST)
# Official Definition v1.1
#
# In memory of Sahadia.

from dataclasses import dataclass
from typing import List, Optional


class ASTNode:
    pass


@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]


# ============
# EXPRESSIONS
# ============

@dataclass
class NumberNode(ASTNode):
    value: float


@dataclass
class StringNode(ASTNode):
    value: str


@dataclass
class IdentifierNode(ASTNode):
    name: str


@dataclass
class BinaryExpressionNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode]


# ============
# STATEMENTS
# ============

@dataclass
class SoulNode(ASTNode):
    message: ASTNode


@dataclass
class SayNode(ASTNode):
    message: ASTNode


@dataclass
class RememberNode(ASTNode):
    name: str
    value: ASTNode


@dataclass
class AskNode(ASTNode):
    question: ASTNode
    target: str


@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class RepeatNode(ASTNode):
    times: ASTNode
    body: List[ASTNode]


@dataclass
class UseNode(ASTNode):
    library_name: str


@dataclass
class FunctionNode(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]


@dataclass
class ReturnNode(ASTNode):
    value: ASTNode
