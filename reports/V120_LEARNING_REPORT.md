# V120 Learning Report

Promoted `branch_rhs_arith_const_print_select_fusion`, the residual constant-LHS right-hand arithmetic family for `Number cmp (Var op Number)` with `+`, `-`, `*`, `/`, all six comparisons, and exactly one Number/Var print per arm. Literal-zero division is deliberately excluded. Selected variable print arms remain lazy.

Verification: **8,064/8,064** bounded differential cases; **5,000/5,000** deterministic fuzz cases (seed 120); two lazy missing-variable guards; literal-zero division negative matcher/error-equivalence guard; complete workspace **1,077/1,077** pytest cases.

The unchanged **194-case executable corpus** passed with zero correctness failures and zero regressions. It contains no v120 target, so **0 corpus cases improved** and aggregate means remain unchanged (bytecode ops **1.830 -> 1.830**, VM steps **1.892 -> 1.892**). A direct matching target compiles to **1 opcode / 1 VM step**.

The v112-v119 select families and previously saturated modulo/division-expression, CSE, branch-local propagation, and copy/store batching experiments were not replayed. `Var cmp (arithmetic RHS)`, generic expression print arms, and multi-statement arms remain prefiltered pending explicit effect/exception analysis.

Decision: **promote v120 locally**. The full local workspace is authoritative; this report publishes verification evidence to the compact remote repository.
