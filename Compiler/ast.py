# 🕊️ SAHADIA LANGUAGE
# Abstract Syntax Tree (AST)
# Official Definition v1.0
#
# In memory of Sahadia.

from dataclasses import dataclass
from typing import List, Optional, Any


# =========================
# BASE NODES
# =========================

class ASTNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]


# =========================
# EXPRESSIONS
# =========================

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


# =========================
# STATEMENTS
# =========================

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


# =========================
# FUNCTIONS & LIBRARIES
# =========================

@dataclass
class FunctionNode(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]


@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode]


@dataclass
class UseNode(ASTNode):
    library_name: str


# =========================
# BUILD / CREATE (EXTENSIBLE)
# =========================

@dataclass
class BuildNode(ASTNode):
    target: str
    body: List[ASTNode]


@dataclass
class CreateNode(ASTNode):
    target: str
    body: List[ASTNode]
