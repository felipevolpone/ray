import unittest
from alabamaonhands.all import AlabamaModel


class TestAlabamaModel(unittest.TestCase):

    def test(self):
        model = AlabamaModel()
        self.assertTrue(hasattr(model, 'put'))
        self.assertTrue(hasattr(model, 'delete'))

