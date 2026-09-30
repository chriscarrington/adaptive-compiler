from pathlib import Path
import pytest
from adaptive_compiler.learner import Learner
from adaptive_compiler.compiler import compile_source
from adaptive_compiler.vm import VM

POLICY = Learner(Path('state/ongoing_model.json')).policy()

def run(src, env):
    p=compile_source(src, POLICY); vm=VM(); out=vm.run(p.code, env); return out,p,vm

@pytest.mark.parametrize('x,m', [(x,m) for x in range(-8,9) for m in range(-5,6) if m])
def test_mod_var_nested_differential(x,m):
    out,p,vm=run('x = input0; m = input1; print((x % m) + 1);', {'input0':x,'input1':m})
    assert out == (x % m)+1
    assert any(i[0]=='MOD_VAR' for i in p.code)

@pytest.mark.parametrize('x,m', [(x,m) for x in range(-8,9) for m in (-5,-2,-1,1,2,5)])
def test_mod_const_nested_differential(x,m):
    src=f'x = input0; print((x % {m}) + 1);'
    out,p,vm=run(src, {'input0':x})
    assert out == (x % m)+1
    assert any(i[0]=='MOD_CONST' for i in p.code)

def test_print_mod_const_direct_fuses():
    out,p,vm=run('x = input0; print(x % 5);', {'input0':18})
    assert out == 3
    assert p.code == [('PRINT_MOD_CONST','input0',5)]
