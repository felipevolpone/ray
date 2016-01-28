import unittest
import requests
from onhandsalabama.all import AlabamaModel
from alabama import connection


class TestLoader(unittest.TestCase):
    def setUp(self):
        database = connection.start_db('tests/db.properties')
        connection.create_pool(database)


class TestIntegration(TestLoader):
    def test_api(self):
        resp = requests.post('http://localhost:8080/api/user',
                          json={'name':'felipe','age':23})
        self.assertEqual(200, resp.status_code)
