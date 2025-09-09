import unittest

from src.bospy import bos

class TestBasicQuery(unittest.TestCase):
    def setUp(self):
        bos.SYSMOD_ADDR = "nuc.local:3821"
        self.basic_query = """
        SELECT DISTINCT ?subject ?predicate ?object
                WHERE {
                    BIND(<bos://localhost/dev/1> AS ?startNode)
                    {
                        ?startNode ?predicate ?object .
                        BIND(?startNode AS ?subject)
                    }
                    UNION
                    {
                        ?subject ?predicate ?startNode .
                        BIND(?startNode AS ?object)
                    }
                }
"""
    def test_basic_query(self):
        g = bos.BasicQuery(self.basic_query)
        print(g.all_nodes())

if __name__ == '__main__':
    
    unittest.main()