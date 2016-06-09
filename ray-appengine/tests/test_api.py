
import unittest
from ray_appengine.all import *


class TestApi(unittest.TestCase):

	def test_columns(self):
		m = GAEModel()
		self.assertEqual(m.columns(), ['nome'])

	def test_put(self):
		m = GAEModel(name="any")
		self.assertIsNotNone(m.put())