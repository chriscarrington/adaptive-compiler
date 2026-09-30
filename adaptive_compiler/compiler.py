from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class Program:
    code: list[tuple]

def _atom(s):
    s=s.strip()
    while s.startswith("(") and s.endswith(")"): s=s[1:-1].strip()
    if re.fullmatch(r"-?\d+",s): return ("const",int(s))
    return ("var",s)

def compile_source(source, policy=None):
    policy=set(policy or ())
    code=[]
    for raw in source.split(";"):
        s=raw.strip()
        if not s: continue
        m=re.fullmatch(r"print\((.*)\)",s)
        if m:
            e=m.group(1).strip()
            mm=re.fullmatch(r"([A-Za-z_]\w*)\s*%\s*(-?\d+)",e)
            if mm and "print_mod_const_fusion" in policy:
                code.append(("PRINT_MOD_CONST",mm.group(1),int(mm.group(2)))); continue
            code.append(("PRINT_EXPR",e)); continue
        m=re.fullmatch(r"([A-Za-z_]\w*)\s*=\s*(.*)",s)
        if m: code.append(("ASSIGN_EXPR",m.group(1),m.group(2).strip())); continue
        raise SyntaxError(f"unsupported statement: {s}")
    return Program(code)
