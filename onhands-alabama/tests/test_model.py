import unittest
from onhandsalabama.all import AlabamaModel
from alabama import connection


class TestAlabamaModel(unittest.TestCase):
    def test(self):
        model = AlabamaModel()
        self.assertTrue(hasattr(model, 'put'))
        self.assertTrue(hasattr(model, 'delete'))
