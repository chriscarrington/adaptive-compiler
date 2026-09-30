# V113 Learning Report

Promoted `branch_print_var_select_fusion`, a narrow variable-arm sibling of v112. It accepts direct comparisons where both branches contain exactly one `print(Var)`. The VM reads only the selected arm variable, preserving branch laziness.

Verification: 1680/1680 bounded accepted-shape differential cases, 2/2 lazy-arm guards, 1049/1049 full local tests, and 194/194 corpus semantic equivalence with zero regressions. The fixed corpus contains no matching case, so improved corpus cases are zero. The direct target improves from 4 ops / 3 steps to 1 / 1.

The residual frontier was refreshed rather than replaying saturated modulo, division, CSE, branch-local propagation, or broad copy batching experiments. Broader expression-arm select was prefiltered for eager-evaluation/error risk; mixed constant/variable arms remain a separate bounded frontier.

Decision: promoted and persisted in the full local workspace. GitHub publication is an isolated reproduction layer because the earlier remote repository was a compact reconstruction rather than the complete historical workspace.
