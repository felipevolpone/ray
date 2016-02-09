import unittest, requests, json
# from onhandsalabama.all import AlabamaModel


def jsonify(data):
    return json.dumps(data)


class TestIntegration(unittest.TestCase):

    def test_api(self):
        resp = requests.post('http://localhost:8080/api/user',
                             data=jsonify({'name': 'felipe', 'age': 23}))
        returned = resp.json()
        uuid = returned['result']['uuid']
        self.assertEqual('felipe', returned['result']['name'])
        self.assertEqual(23, returned['result']['age'])
        self.assertEqual(200, resp.status_code)

        resp = requests.get('http://localhost:8080/api/user')
        self.assertEqual(200, resp.status_code)
        returned = resp.json()

        self.assertEqual(1, len(returned['result']))
        self.assertEqual('felipe', returned['result'][0]['name'])
        self.assertEqual(23, returned['result'][0]['age'])
        self.assertEqual(uuid, returned['result'][0]['uuid'])

        resp = requests.get('http://localhost:8080/api/user/' + uuid)
        returned = resp.json()
        self.assertEqual(200, resp.status_code)
        self.assertEqual('felipe', returned['result']['name'])
        self.assertEqual(23, returned['result']['age'])
        self.assertEqual(uuid, returned['result']['uuid'])

        resp = requests.delete('http://localhost:8080/api/user/' + uuid)
        self.assertEqual(200, resp.status_code)
        returned = resp.json()
        self.assertEqual(returned['result'], [])

        resp = requests.get('http://localhost:8080/api/user/' + uuid)
        self.assertEqual(404, resp.status_code)
