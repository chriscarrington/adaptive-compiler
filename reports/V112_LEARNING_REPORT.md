# V112 Learning Report

Promoted `branch_print_select_fusion` for the deliberately narrow shapes `if x cmp C { print(A); } else { print(B); }` and `if x cmp y { print(A); } else { print(B); }`, with six comparison operators and constant print arms only.

Local verification passed 1046/1046 tests. The dedicated bounded differential suite passed 504 accepted-shape cases plus two negative matcher guards. The unchanged 194-case corpus had zero correctness failures and zero regressions, with 27 improved cases. Mean bytecode ops improved from 2.44845 to 2.03093 and mean VM steps from 2.30412 to 2.02577. The direct target improved from 4 ops / 3 steps to 1 / 1.

The GitHub CI layer is intentionally an isolated reproduction harness rather than a claim that the earlier recovered repository snapshot is byte-for-byte identical to the full local workspace. It rechecks the promoted transformation across Linux, Windows, and macOS on Python 3.11, 3.12, and 3.13.
