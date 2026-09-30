# V111 Learning Report

## Verified change
Repaired missing VM execution support for the already-defined `MOD_CONST` and `MOD_VAR` expression opcodes, then promoted only the modulo hypotheses that materially improve the mature policy: `expr_mod_const_fusion`, `expr_mod_var_fusion`, and `print_mod_const_fusion`.

## Residual frontier and prefilter
The refreshed v110 residual scan exposed modulo expression targets at 6 ops / 6 steps and direct modulo print at 4 / 4. Trial activation initially failed because the compiler could emit `MOD_CONST` / `MOD_VAR` but the VM had no handlers. After repairing that dormant-path inconsistency, the three useful hypotheses were evaluated. `store_mod_const_fusion` and `store_mod_var_fusion` were not promoted: their direct toggles are composition-shadowed by the mature `STORE_PRINT` path and add no target benefit.

## Bounds and correctness
- Full expanded deterministic suite: **540/540 passed**.
- New bounded modulo differential domain: **272/272 passed**.
- Divisor zero is excluded from generated modulo cases; constant matcher already guards zero constants.
- Executable example corpus: **194 cases, 0 correctness failures**.
- Corpus regressions: **0**.
- Mean bytecode ops: **2.50515 -> 2.44845**.
- Mean VM steps: **2.36082 -> 2.30412**.
- `expr_mod_const_fusion`: **6/6 -> 4/4**.
- `expr_mod_var_fusion`: **6/6 -> 4/4**.
- `print_mod_const_fusion`: **4/4 -> 1/1**.

## Promotion decision
**Promoted.** Three previously dormant modulo rules are now enabled only after VM semantics, bounded differential coverage, full tests, and corpus audit passed. Store-modulo rules remain disabled because their standalone target evidence is composition-shadowed and therefore not independently informative.
