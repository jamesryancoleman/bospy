import src.bospy.bos as bos
import unittest

class TestGetLocations(unittest.TestCase):
    def test_get_all(self):
        results = bos.GetAllLocation()
        print(results)

    # def test_get_all_triples(self):
    #     results = bos.GetAllLocation()
    #     for row in results:
    #         print(row) 