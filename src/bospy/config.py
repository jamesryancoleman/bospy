import os
import warnings

_default_orchestrator_addr = "localhost:2824"
_orchestrator_addr = os.environ.get("ORCHESTRATOR_ADDR", _default_orchestrator_addr)

def set_orchestrator_addr(addr:str):
    global _orchestrator_addr
    _orchestrator_addr = addr

def get_orchestrator_addr():
    if _orchestrator_addr == _default_orchestrator_addr:
        warnings.warn(f"orchestrator address not set. Default used ({_default_orchestrator_addr})")
    return _orchestrator_addr