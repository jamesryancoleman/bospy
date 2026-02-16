import bospy.config as config

DEBUG = True

if __name__  == "__main__":
    if DEBUG:
        _config = {
            "sysmod": config.get_sysmod_addr(),
            "devctrl": config.get_devctrl_addr(),
            "history": config.get_history_addr(),
            "orchestrator": config.get_orchestrator_addr(), 
            "forecast": config.get_forecast_addr(),
        }
        print(_config)