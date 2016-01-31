import unittest
import requests
# from onhandsalabama.all import AlabamaModel


class TestIntegration(unittest.TestCase):
    def test_api(self):
        resp = requests.post('http://localhost:8080/api/user',
                             data={'name': 'felipe', 'age': 23})
        self.assertEqual(200, resp.status_code)

        resp = requests.get('http://localhost:8080/api/user')
        self.assertEqual(200, resp.status_code)
