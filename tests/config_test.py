import bospy.config as config
import unittest
import os

class TestConfig(unittest.TestCase):
    def setUp(self):
        os.environ["SYSMOD_ADDR"] = "nuc:2821"
        os.environ["DEVCTRL_ADDR"] = "nuc:2822"
        os.environ["HISTORY_ADDR"] = "nuc:2823"
        os.environ["ORCHESTRATOR_ADDR"] = "nuc:2824"
        os.environ["FORECAST_ADDR"] = "nuc:2825"
    
    def test_01_load_defaults(self):
        print("== default ==")
        print(f'sysmod:       {config.get_sysmod_addr()}')
        print(f'devctrl:      {config.get_devctrl_addr()}')
        print(f'history:      {config.get_history_addr()}')
        print(f'orchestrator: {config.get_orchestrator_addr()}')
        print(f'sysmod:       {config.get_forecast_addr()}')

    def test_02_load_env(self):
        config.from_env()
        print("== env ==")
        print(f'sysmod:       {config.get_sysmod_addr()}')
        print(f'devctrl:      {config.get_devctrl_addr()}')
        print(f'history:      {config.get_history_addr()}')
        print(f'orchestrator: {config.get_orchestrator_addr()}')
        print(f'sysmod:       {config.get_forecast_addr()}')

    def test_03_set_addr(self):
        config.set_sysmod_addr("nonsense:1")
        config.set_devctrl_addr("nonsense:2")
        config.set_history_addr("nonsense:3")
        config.set_orchestrator_addr("nonsense:4")
        config.set_forecast_addr("nonsense:5")

        print("== manual ==")        
        print(f'sysmod:       {config.get_sysmod_addr()}')
        print(f'devctrl:      {config.get_devctrl_addr()}')
        print(f'history:      {config.get_history_addr()}')
        print(f'orchestrator: {config.get_orchestrator_addr()}')
        print(f'sysmod:       {config.get_forecast_addr()}')
        

    def tearDown(self):
        # return super().tearDown()
        pass