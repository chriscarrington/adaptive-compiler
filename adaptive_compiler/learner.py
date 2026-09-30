from __future__ import annotations
import json
class Learner:
    def __init__(self,path): self.path=path
    def policy(self):
        try:
            data=json.loads(self.path.read_text())
            return set(data.get("enabled",data.get("policy",{}).get("enabled",[])))
        except FileNotFoundError:
            return {"expr_mod_const_fusion","expr_mod_var_fusion","print_mod_const_fusion"}
