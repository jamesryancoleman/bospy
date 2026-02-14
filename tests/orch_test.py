from bospy.config import set_orchestrator_addr, get_orchestrator_addr
import bospy.orch as orch
import unittest
import time

class TestRun(unittest.TestCase):
    def setUp(self):
       pass

    def test_01_run(self):
        orch.run('thinker', envVars={
            'lower_bound': 10,
            'upper_bound': 100,
            'minutes':  0.5
        }, timeout=-1)

class TestGetRunning(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_run(self):
        # launch an app
        for i in range(3):
            resp = orch.run('thinker', envVars={
                'lower_bound': 10,
                'upper_bound': 100,
                'minutes':  0.2
            }, timeout=-1)
            print(f'the id of job_{i+1} is: {resp.Header.TxnId}')
            time.sleep(0.1)

        # check what's running
        jobs = orch.get_running_apps()
        print(f'there are {len(jobs)} running.')
        print(jobs)


    def test_02_run(self):
        # wait for the apps to exit then check again
        time.sleep(0.3 * 60)
        
        # check what's running
        jobs = orch.get_running_apps()
        print(f'there are {len(jobs)} running.')
        print(jobs)

class TestStopRunning(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_stop_running(self):
        for i in range(3):
            resp = orch.run('thinker', envVars={
                'lower_bound': 10,
                'upper_bound': 100,
                'minutes':  0.2
            }, timeout=-1)
            print(f'the id of job_{i+1} is: {resp.Header.TxnId}')
            time.sleep(0.1)
        
        # check what's running
        jobs = orch.get_running_apps()
        print(f'there are {len(jobs)} running.')
        print(jobs)
        orch.stop_apps(jobs.keys())    

    
