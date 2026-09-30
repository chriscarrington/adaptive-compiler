from __future__ import annotations
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Number:
    value: int | float

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Binary:
    op: str
    left: "Expr"
    right: "Expr"

@dataclass(frozen=True)
class Assign:
    name: str
    value: "Expr"

@dataclass(frozen=True)
class Print:
    value: "Expr"

@dataclass(frozen=True)
class Block:
    statements: tuple["Stmt", ...]

@dataclass(frozen=True)
class If:
    condition: "Expr"
    then_block: Block
    else_block: Block | None

@dataclass(frozen=True)
class While:
    condition: "Expr"
    body: Block

Expr = Union[Number, Var, Binary]
Stmt = Union[Assign, Print, If, While]
