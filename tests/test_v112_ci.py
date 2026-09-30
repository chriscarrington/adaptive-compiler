import pytest
from adaptive_compiler.compiler import compile_source
from adaptive_compiler.vm import VM

OPS=("==","!=",">","<","<=",">=")

def run(src, policy, env):
    p=compile_source(src,policy); vm=VM(); out=vm.run(p.code,env); return out,p,vm

@pytest.mark.parametrize("op",OPS)
@pytest.mark.parametrize("x",range(-3,4))
@pytest.mark.parametrize("c",range(-2,3))
def test_const_rhs_v112_differential(op,x,c):
    src=f"if x {op} {c} {{ print(17); }} else {{ print(-4); }}"
    base,bp,bv=run(src,{},{"x":x})
    cand,cp,cv=run(src,{"branch_print_select_fusion":True},{"x":x})
    assert cand==base
    assert cp.code==[("PRINT_SELECT_CMP_CONST",op,"x",c,17,-4)]
    assert len(bp.code)==4
    assert cv.steps==1

@pytest.mark.parametrize("op",OPS)
@pytest.mark.parametrize("x",range(-3,4))
@pytest.mark.parametrize("y",range(-3,4))
def test_var_rhs_v112_differential(op,x,y):
    src=f"if x {op} y {{ print(17); }} else {{ print(-4); }}"
    base,bp,bv=run(src,{},{"x":x,"y":y})
    cand,cp,cv=run(src,{"branch_print_select_fusion":True},{"x":x,"y":y})
    assert cand==base
    assert cp.code==[("PRINT_SELECT_CMP_VAR",op,"x","y",17,-4)]
    assert len(bp.code)==4
    assert cv.steps==1

def test_nonconstant_arm_is_not_accepted_by_narrow_matcher():
    with pytest.raises(SyntaxError):
        compile_source("if x > 0 { print(x); } else { print(0); }",{"branch_print_select_fusion":True})

def test_assignment_arm_is_not_accepted_by_narrow_matcher():
    with pytest.raises(SyntaxError):
        compile_source("if x > 0 { y=1; print(1); } else { print(0); }",{"branch_print_select_fusion":True})
