from adaptive_compiler.compiler import _enabled, Program
from adaptive_compiler.vm import _cmp

RULE = "branch_print_var_select_fusion"

def compile_v113_select(op, left, right, then_name, else_name, right_is_var=False, policy=None):
    if not _enabled(policy, RULE):
        raise ValueError("v113 rule disabled")
    opcode = "PRINT_VAR_SELECT_CMP_VAR" if right_is_var else "PRINT_VAR_SELECT_CMP_CONST"
    return Program([(opcode, op, left, right, then_name, else_name)])

def execute_v113_select(instruction, env):
    op, cmpop, left, right, then_name, else_name = instruction
    rhs = env[right] if op.endswith("_VAR") else right
    return env[then_name] if _cmp(cmpop, env[left], rhs) else env[else_name]
