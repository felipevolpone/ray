
import unittest, requests
from .app import User
import json

class TestIntegrated(unittest.TestCase):

    def test_columns(self):
        columns = User.columns()
        self.assertEqual(['age', 'id', 'name'], columns)

    def test_api(self):
        data = json.dumps({'age': 22, 'name': 'felipe'})
        resp = requests.post('http://localhost:8080/api/user', data=data)   
        self.assertEqual({u'result': {u'age': 22, u'name': 'felipe'}}, resp.json())
