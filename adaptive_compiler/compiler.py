from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class Program:
    code: list[tuple]

def _enabled(policy, rule):
    if isinstance(policy, dict):
        return bool(policy.get(rule, False))
    return rule in set(policy or ())

def compile_source(source, policy=None):
    source=source.strip()
    # CI/reproduction path for the verified v112 narrow branch-print select rule.
    # It intentionally accepts only direct variable comparisons with one constant
    # print in each arm.
    branch=re.fullmatch(
        r"if\s+([A-Za-z_]\w*)\s*(==|!=|<=|>=|<|>)\s*"
        r"(-?\d+|[A-Za-z_]\w*)\s*\{\s*print\((-?\d+)\);\s*\}"
        r"\s*else\s*\{\s*print\((-?\d+)\);\s*\}\s*;?",
        source,
    )
    if branch:
        left,op,right,then_v,else_v=branch.groups()
        then_v=int(then_v); else_v=int(else_v)
        if re.fullmatch(r"-?\d+",right):
            right=int(right)
            if _enabled(policy,"branch_print_select_fusion"):
                return Program([("PRINT_SELECT_CMP_CONST",op,left,right,then_v,else_v)])
            return Program([
                ("JUMP_IF_CMP_CONST_FALSE",op,left,right,3),
                ("PRINT_CONST",then_v),
                ("JUMP",4),
                ("PRINT_CONST",else_v),
            ])
        if _enabled(policy,"branch_print_select_fusion"):
            return Program([("PRINT_SELECT_CMP_VAR",op,left,right,then_v,else_v)])
        return Program([
            ("JUMP_IF_CMP_VAR_FALSE",op,left,right,3),
            ("PRINT_CONST",then_v),
            ("JUMP",4),
            ("PRINT_CONST",else_v),
        ])

    # Preserve the previously published compact modulo reproduction interface.
    code=[]
    for raw in source.split(";"):
        s=raw.strip()
        if not s: continue
        m=re.fullmatch(r"print\((.*)\)",s)
        if m:
            e=m.group(1).strip()
            mm=re.fullmatch(r"([A-Za-z_]\w*)\s*%\s*(-?\d+)",e)
            if mm and _enabled(policy,"print_mod_const_fusion"):
                code.append(("PRINT_MOD_CONST",mm.group(1),int(mm.group(2)))); continue
            code.append(("PRINT_EXPR",e)); continue
        m=re.fullmatch(r"([A-Za-z_]\w*)\s*=\s*(.*)",s)
        if m:
            code.append(("ASSIGN_EXPR",m.group(1),m.group(2).strip())); continue
        raise SyntaxError(f"unsupported statement: {s}")
    return Program(code)
