
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
        result = json.loads(resp.content)['result']
        self.assertEqual(result['name'], 'felipe')
        self.assertEqual(result['age'], 22)

        self.assertIsNotNone(result['id'])
        id_created = str(result['id'])

        resp = requests.get('http://localhost:8080/api/user')
        result = json.loads(resp.content)['result']
        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 22)
        self.assertIsNotNone(result[0]['id'])

        resp = requests.delete('http://localhost:8080/api/user/' + id_created)
        print resp.json()
        result = json.loads(resp.content)['result']
        self.assertEqual(id_created, result['id'])
