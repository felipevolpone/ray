
import unittest
from ray_appengine.all import *
from pprint import pprint

class TestApi(unittest.TestCase):

	def test_api(self):
		m = GAEModel()
		#pprint(dir(m))
		self.assertEqual(m.columns(), ['nome'])
