import os
import logging

logger = logging.getLogger(__name__)

_default_sysmod_addr = "sysmod:2821"
_sysmod_addr = os.environ.get('SYSMOD_ADDR', _default_sysmod_addr)

_default_devctrl_addr = "devctrl:2822"
_devctrl_addr = os.environ.get('DEVCTRL_ADDR', _default_devctrl_addr)

_defaul_history_addr = "history:2823"
_history_addr = os.environ.get('HISTORY_ADDR', _defaul_history_addr)

_default_orchestrator_addr = "orchestrator:2824"
_orchestrator_addr = os.environ.get("ORCHESTRATOR_ADDR", _default_orchestrator_addr)

_default_forecast_addr = "forecast:2825"
_forecast_addr = os.environ.get('FORECAST_ADDR', _default_forecast_addr)

def from_env():
    global _sysmod_addr, _devctrl_addr, _history_addr, _orchestrator_addr, _forecast_addr
    _sysmod_addr = os.environ.get('SYSMOD_ADDR', _default_sysmod_addr)
    _devctrl_addr = os.environ.get('DEVCTRL_ADDR', _default_devctrl_addr)
    _history_addr = os.environ.get('HISTORY_ADDR', _defaul_history_addr)
    _orchestrator_addr = os.environ.get("ORCHESTRATOR_ADDR", _default_orchestrator_addr)
    _forecast_addr = os.environ.get('FORECAST_ADDR', _default_forecast_addr)

def get_config() -> dict[str,str]:
    return {
            "SYSMOD_ADDR": get_sysmod_addr(),
            "DEVCTRL_ADDR": get_devctrl_addr(),
            "HISTORY_ADDR": get_history_addr(),
            "ORCHESTRATOR_ADDR": get_orchestrator_addr(), 
            "FORECAST_ADDR": get_forecast_addr(),
        }

def set_sysmod_addr(addr:str):
    global _sysmod_addr
    _sysmod_addr = addr

def get_sysmod_addr():
    if _sysmod_addr == _default_sysmod_addr:
        logger.warning(f"sysmod address not set. Default used ({_default_sysmod_addr})")
    return _sysmod_addr

def set_devctrl_addr(addr:str):
    global _devctrl_addr
    _devctrl_addr = addr

def get_devctrl_addr():
    if _devctrl_addr == _default_devctrl_addr:
        logger.warning(f"devctrl address not set. Default used ({_default_devctrl_addr})")
    return _devctrl_addr

def set_history_addr(addr:str):
    global _history_addr
    _history_addr = addr

def get_history_addr():
    if _history_addr == _defaul_history_addr:
        logger.warning(f"history address not set. Default used ({_defaul_history_addr})")
    return _history_addr

def set_orchestrator_addr(addr:str):
    global _orchestrator_addr
    _orchestrator_addr = addr

def get_orchestrator_addr():
    if _orchestrator_addr == _default_orchestrator_addr:
        logger.warning(f"orchestrator address not set. Default used ({_default_orchestrator_addr})")
    return _orchestrator_addr

def set_forecast_addr(addr:str):
    global _forecast_addr
    _forecast_addr = addr

def get_forecast_addr():
    if _forecast_addr == _default_forecast_addr:
        logger.warning(f"forecast address not set. Default used ({_default_forecast_addr})")
    return _forecast_addr
