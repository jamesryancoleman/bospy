from bospy import bos
import unittest

class TestHistory(unittest.TestCase):
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

    def test_history(self):
        HistoryTest(self.test_uris[0])

def HistoryTest(bosPtUri:str|list[str]):
    df = bos.GetHistory(bosPtUri, pandas=True, limit=25)
    print(df)


if __name__ == "__main__":
    unittest.main()

