from .common import Test


class TestEndpoint(Test):

    def testing_wrong_endpoints(self):
        response = self.app.get('/api/', expect_errors=True)
        self.assertEqual(404, response.status_int)

        response = self.app.get('/api/wrongurl', expect_errors=True)
        self.assertEqual(404, response.status_int)

    def __create(self):
        return self.app.post_json('/api/user', {"name": "felipe", "age": 22})

    def test_post(self):
        resp = self.__create()
        result = resp.json
        self.assertEqual('felipe', result['result']['name'])
        self.assertEqual(201, resp.status_int)

    def test_get_all(self):
        self.__create()

        resp = self.app.get('/api/user')
        self.assertEqual(200, resp.status_int)

    def test_get(self):
        uuid_created = '1245'
        resp = self.app.get('/api/user/' + uuid_created)
        self.assertEqual(200, resp.status_int)

    def test_put(self):
        uuid_created = '1245'
        response = self.app.put_json('/api/user/' + uuid_created, {"name": "ray", 'uuid': uuid_created})
        self.assertEqual(200, response.status_int)
        self.assertEquals('', response.body.decode('utf-8'))

    def test_delete(self):
        response = self.app.delete('/api/user/1245')
        self.assertEqual(200, response.status_int)
