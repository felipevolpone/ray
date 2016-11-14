
from webtest import TestApp as FakeApp

from ray.endpoint import endpoint
from ray.wsgi.wsgi import application
from ray.authentication import Authentication, register
from ray.shield import Shield

from tests.model_interface import ModelInterface
from .common import Test


global_person_id = None
global_parameters = None


class TestShield(Test):

    def test_shields(self):

        @register
        class MyAuth(Authentication):

            expiration_time = 5
            salt_key = 'ray_salt_key'

            @classmethod
            def authenticate(cls, login_data):
                if login_data['password'] == '123':
                    return {'username': 'felipe'}

        @endpoint('/person', authentication=MyAuth)
        class PersonModel(ModelInterface):

            def __init__(self, *a, **k):
                self.login = None
                super(PersonModel, self).__init__(*a, **k)

            @classmethod
            def columns(cls):
                return ['id']

        class PersonShield(Shield):
            __model__ = PersonModel

            def get(self, user_data, person_id, parameters):
                return user_data['username'] == 'felipe'

            def put(self, user_data, person_id, parameters):
                assert person_id == '1'
                assert parameters == {'any': 'bla@gmail.com'}

                return True

        global global_person_id

        response = self.app.post_json('/api/_login', {"username": "felipe", 'password': '123'})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/person/')
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', {"username": "john", 'password': '123'})
        self.assertEqual(200, response.status_int)

        global global_parameters
        self.app.put_json('/api/person/1/', {'any': 'bla@gmail.com'})
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.get('/api/person', expect_errors=True)
        self.assertEquals(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post('/api/person/', expect_errors=True)
        self.assertIsNot(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.put('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)

        self.app = FakeApp(application)
        response = self.app.delete('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)
