from __future__ import annotations
import ast, operator

_BIN={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,
     ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod}

def _eval(expr,env):
    n=ast.parse(expr,mode="eval").body
    def go(x):
        if isinstance(x,ast.Constant) and isinstance(x.value,(int,float)): return x.value
        if isinstance(x,ast.Name): return env[x.id]
        if isinstance(x,ast.BinOp) and type(x.op) in _BIN: return _BIN[type(x.op)](go(x.left),go(x.right))
        if isinstance(x,ast.UnaryOp) and isinstance(x.op,ast.USub): return -go(x.operand)
        raise ValueError("unsupported expression")
    return go(n)

def _cmp(op,a,b):
    return {"==":a==b,"!=":a!=b,">":a>b,"<":a<b,"<=":a<=b,">=":a>=b}[op]

class VM:
    def __init__(self): self.steps=0
    def run(self,code,env=None):
        env=dict(env or {}); out=None; self.steps=0; pc=0
        while pc < len(code):
            self.steps+=1; ins=code[pc]; op=ins[0]
            if op=="ASSIGN_EXPR": env[ins[1]]=_eval(ins[2],env)
            elif op=="PRINT_EXPR": out=_eval(ins[1],env)
            elif op=="PRINT_MOD_CONST": out=env[ins[1]] % ins[2]
            elif op=="MOD_CONST": out=env[ins[1]] % ins[2]
            elif op=="MOD_VAR": out=env[ins[1]] % env[ins[2]]
            elif op=="PRINT_CONST": out=ins[1]
            elif op=="PRINT_SELECT_CMP_CONST":
                _,cmpop,left,right,tv,fv=ins; out=tv if _cmp(cmpop,env[left],right) else fv
            elif op=="PRINT_SELECT_CMP_VAR":
                _,cmpop,left,right,tv,fv=ins; out=tv if _cmp(cmpop,env[left],env[right]) else fv
            elif op=="JUMP_IF_CMP_CONST_FALSE":
                _,cmpop,left,right,target=ins
                if not _cmp(cmpop,env[left],right): pc=target; continue
            elif op=="JUMP_IF_CMP_VAR_FALSE":
                _,cmpop,left,right,target=ins
                if not _cmp(cmpop,env[left],env[right]): pc=target; continue
            elif op=="JUMP": pc=ins[1]; continue
            else: raise ValueError(f"unknown opcode {op}")
            pc+=1
        return out
