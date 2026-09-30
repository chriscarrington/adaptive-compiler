from dataclasses import dataclass
from typing import Any

class Node: pass
@dataclass
class Expr(Node): pass
@dataclass
class Number(Expr): value: int
@dataclass
class Var(Expr): name: str
@dataclass
class Binary(Expr): op: str; left: Expr; right: Expr
@dataclass
class Stmt(Node): pass
@dataclass
class Assign(Stmt): name: str; expr: Expr
@dataclass
class Print(Stmt): expr: Expr
@dataclass
class While(Stmt): cond: Expr; body: list
@dataclass
class If(Stmt): cond: Expr; then_body: list; else_body: list
@dataclass
class Program(Node): statements: list
