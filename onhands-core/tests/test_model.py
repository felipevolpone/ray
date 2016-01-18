from onhands.model import ModelOnHands
import unittest


class TestModelOnHands(unittest.TestCase):

    def test_protocol(self):
        model = ModelOnHands()
        with self.assertRaises(NotImplementedError):
            model.put()

        with self.assertRaises(NotImplementedError):
            model.delete()

