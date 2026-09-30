# adaptive-compiler

Verified adaptive-compiler learning results and reproducibility gates.

## Current verified local state

v112 promotes a narrow `branch_print_select_fusion` for direct variable comparisons whose then/else arms each print exactly one constant. The full local workspace passed 1046/1046 tests and a 194-case corpus audit with zero correctness failures and zero regressions.

## GitHub CI

The repository includes an isolated v112 differential reproduction harness. GitHub Actions runs 506 bounded checks across Linux, Windows, and macOS on Python 3.11, 3.12, and 3.13. This CI harness verifies the promoted transformation independently of the historical generated learner state; the full local workspace remains the authoritative source for the complete 1046-test promotion evidence.

See `reports/V112_LEARNING_REPORT.md` and `reports/V112_LEARNING_RESULT.json`.
