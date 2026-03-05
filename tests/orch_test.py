from bospy.config import set_orchestrator_addr, get_orchestrator_addr, get_config
import bospy.orch as orch
import unittest
import datetime
import time
import os

from zoneinfo import ZoneInfo

_tz = ZoneInfo("America/New_York")

config = get_config()

class TestRun(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_run(self):
        orch.run('thinker', envVars={
            'lower_bound': 10,
            'upper_bound': 100,
            'minutes':  1
        } | {"ORCHESTRATOR_ADDR": "localhost:2824"},
        timeout=-1)

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

class TestSchedule(unittest.TestCase):
    def setUp(self):
        print(f'the orchestrator address is {get_orchestrator_addr()}')

    def test_00_check_running(self):
        # check what's running
        jobs = orch.get_scheduled_apps()
        print(f'there are {len(jobs)} scheduled.')
        print(jobs)

    def test_01_schedule_cron(self):
        # blocks until schedule returns
        resp = orch.schedule("thinker", "*/5 * * * *",
                             on_start=True, 
                             envVars={
                                "ORCHESTRATOR_ADDR":"localhost:2824",
                                "minutes": 5,
                                "lower_bound": 10,
                                "upper_bound": 100,
                                })
        print(resp)
        jobs = orch.get_scheduled_apps()
        print(f'there are {len(jobs)} scheduled.')
        print(jobs)

    def test_02_schedule_job(self): 
        future_dt = datetime.datetime.now(_tz) + datetime.timedelta(seconds=30)
        dt_str = future_dt.isoformat()
        resp = orch.schedule("thinker", dt_str, on_start=False, 
                             envVars={"ORCHESTRATOR_ADDR":"localhost:2824"})
        print(resp)
        jobs = orch.get_scheduled_apps()
        print(f'there are {len(jobs)} scheduled.')
        print(jobs)


    
