
import requests
import json
import unittest
from app import application


class TestExample(unittest.TestCase):

    def test_crud(self):
        description = "Here you can see how to interact with the Ray API"

        data = {"title": "My First Post", "author": "felipe volpone",
                "description": description}
        resp = requests.post('http://localhost:8080/api/post', data=json.dumps(data))
        self.assertIsNotNone(resp.json()['result'])
        post_id = str(resp.json()['result']['id'])

        data = {"username": "felipe", "password": '123'}
        resp = requests.post('http://localhost:8080/api/_login', data=json.dumps(data))
        self.assertEqual(200, resp.status_code)

        cookie = {'RayAuth': resp.cookies['RayAuth']}

        data = {'title': "Changing the title"}
        resp = requests.put('http://localhost:8080/api/post/' + post_id, cookies=cookie, data=json.dumps(data))
        self.assertEqual(200, resp.status_code)

        resp = requests.get('http://localhost:8080/api/post/' + post_id)
        self.assertEqual(200, resp.status_code)
        self.assertEqual('Changing the title', resp.json()['result']['title'])

        data = {'title': "TRYING to Changing the title"}
        resp = requests.put('http://localhost:8080/api/post/' + post_id, data=json.dumps(data))
        self.assertEqual(500, resp.status_code)

        url = 'http://localhost:8080/api/post/' + post_id + '/upper'
        resp = requests.post(url)
        self.assertEqual(200, resp.status_code)

        resp = requests.get('http://localhost:8080/api/post/' + post_id)
        self.assertEqual(200, resp.status_code)
        self.assertEqual('CHANGING THE TITLE', resp.json()['result']['title'])

    def test_hook(self):
        # hooks
        data = {"author": "felipe volpone", "description": "any"}
        resp = requests.post('http://localhost:8080/api/post', data=json.dumps(data))
        self.assertEqual(500, resp.status_code)
