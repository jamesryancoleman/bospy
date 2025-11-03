from bospy import bos, utils
import unittest

class TestGet(unittest.TestCase):
    def setUp(self):
        """ This test currently requires the boptest driver to be running
        """
        self.test_uris = [
            "bos://localhost/dev/12/pts/1",
            "bos://localhost/dev/12/pts/2",
            "bos://localhost/dev/12/pts/3",
            "bos://localhost/dev/12/pts/4"
        ]

    def test_get_env(self):
        print(f"sysmod_addr: {bos.SYSMOD_ADDR}")
        print(f"devctrl_addr: {bos.DEVCTRL_ADDR}")
        print(f"history_addr: {bos.HISTORY_ADDR}")

    def test_get(self):
        GetTest(self.test_uris)

def GetTest(bosPtUri:str|list[str]):
    values = bos.Get(bosPtUri)
    for k, v in values.items():
        print(k, "->", v, "({})".format(type(v)))
    
def GetMultipleTest(bosPtUris:list[str]):
    R = bos.Get(bosPtUris)
    for key, value in R.items():
        print(key, "->", value, "({})".format(type(value)))

if __name__ == "__main__":
    unittest.main()