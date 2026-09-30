# Adaptive Compiler

Verified adaptive compiler baseline. Current promoted learning state: **v111**.

Run the test suite with `python -m pytest -q`.

Verification evidence is retained under `reports/`. Experimental rules are not promoted unless they pass deterministic, bounded differential/fuzz, and corpus audit gates.
