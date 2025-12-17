from bospy import bos
import unittest

class TestForecast(unittest.TestCase):
    def setUp(self):
        """ This test currently requires the boptest driver to be running
        """
        self.test_uri = "bos://localhost/dev/12/pts/1"

    def test_get_env(self):
        print(f"forecast_addr: {bos.FORECAST_ADDR}")

    def test_get_forecast(self):
        GetForecastTest(self.test_uri)

def GetForecastTest(bosPtUri:str):
    df = bos.GetForecast(bosPtUri, pandas=True)
    print(df)


if __name__ == "__main__":
    unittest.main()