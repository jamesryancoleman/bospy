from bospy import bos
import unittest
import time

from typing import Any

class TestSet(unittest.TestCase):
    def setUp(self):
        """ This test currently requires the boptest driver to be running
        """
        self.flow = "bos://localhost/dev/12/pts/6" # air flow (actual)
        self.flowStPt =  "bos://localhost/dev/12/pts/15" # air flow setpoint
        self.flowOverride = "bos://localhost/dev/12/pts/14" # air flow override

    def test_override(self):
        print()
        # confirm starting fan speed
        flow = bos.Get(self.flow)
        print(f"starting fan flow is: {flow}")

        # override the fan
        results = bos.Set(
            [self.flowOverride, self.flowStPt], # keys
            [1, 0.75])                          # values
        print(results)
        
        # wait for override to apply
        time.sleep(16)

        # confirm new fan speed
        flow = bos.Get(self.flow)
        print(f"new fan flow is: {flow}")

        # return to original state
        # override the fan
        results = bos.Set(
            [self.flowOverride, self.flowStPt], # keys
            [0, 0.5])                           # values
        print(results)

def SetTest(bosPtUri:str, value:str):
    ok = bos.Set(bosPtUri, value)
    if ok:
        print(bosPtUri, "<-", value, "(ok)")
    else:
        print(bosPtUri, "<-", value, "(SetError)")

def SetMultipleTest(keys:list[str], values:list[Any]):
    R = bos.Set(keys, values, full_response=True)
    for r in R:
        bosPtUri = r.Key
        valueStr = r.ValueStr # drivers are not required to provide this in response
        if r.Ok:
            print(bosPtUri, "<-", valueStr, "(ok)")
        else:
            print(bosPtUri, "<-", valueStr, "(SetError)")

if __name__ == "__main__":
    # print("sysmod address: ", bos.SYSMOD_ADDR)
    # print("devctrl address:", bos.DEVCTRL_ADDR)
    
    pt1 = "bos://localhost/dev/1/pts/1"
    SetTest(pt1, 420)

    pt2 = "bos://localhost/dev/1/pts/2"
    pt3 = "bos://localhost/dev/1/pts/4"
    pt4 = "bos://localhost/dev/1/pts/5"
    SetMultipleTest(
        [pt2, pt3, pt4],
        [18, 80, True],
        )
    
    # if n pts and 1 value are passed, the value is assigned to all n pts
    SetMultipleTest(
         [pt2, pt3], 
         20
    )

    pt5 = "bos://localhost/dev/2/pts/2"
    SetTest(pt5, False)
