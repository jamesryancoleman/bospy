import bospy.config as config
import unittest
import os

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_01_load_default(self):
        orch_addr = config.get_orchestrator_addr()
        print(f'the default orchestator addr is: {orch_addr}')
        

    def test_02_load_env(self):
        os.environ["ORCHESTRATOR_ADDR"] = "nuc:2824"
        config.set_orchestrator_addr(os.environ.get("ORCHESTRATOR_ADDR"))
        orch_addr = config.get_orchestrator_addr()
        print(f'the env orchestator addr is: {orch_addr}')

    def test_03_set_addr(self):
        config.set_orchestrator_addr("nuc.local:2824")
        orch_addr = config.get_orchestrator_addr()
        print(f'the manually set orchestator addr is: {orch_addr}')
        

    def tearDown(self):
        # return super().tearDown()
        pass