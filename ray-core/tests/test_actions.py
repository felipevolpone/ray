import unittest

from webapp2 import Request

from ray.wsgi.wsgi import application
from ray.actions import ActionAPI, action
from ray.endpoint import endpoint
from ray.shield import Shield

from tests.model_interface import ModelInterface


@endpoint('/user')
class UserModel(ModelInterface):

    def __init__(self, *a, **k):
        self.name = None
        self.age = None
        super(UserModel, self).__init__(*a, **k)

    def describe(self):
        return {'name': str, 'age': int}


any_number = 10


class UserShield(Shield):
    __model__ = UserModel

    @classmethod
    def protect_enable(cls, info):
        return True

    @classmethod
    def protect_fail(cls, info):
        return False


class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("/activate")
    def activate_user(self, model_id):
        # just to make sure that this method was called
        global any_number
        any_number = model_id
        return 'activate_user'

    @action("/<id>/activate_with_id")
    def activate_user_with_id(self, model_id):
        # just to make sure that this method was called
        global any_number
        any_number = model_id
        return 'activate_user'

    # to test Shileds with Actions
    @action('/enable', protection=UserShield.protect_enable)
    def enable_user(self, model_id):
        global any_number
        any_number = 'enabled'

    @action('/enable_fail', protection=UserShield.protect_fail)
    def enable_fail(self, model_id):
        pass


class TestAction(unittest.TestCase):

    def test_get_action(self):
        self.assertEqual('activate_user', ActionAPI('/user/activate', None).process_action())
        # self.assertEqual('activate_user', ActionAPI('/user/123/activate', '123').process_action())

    def test_action(self):
        user_id = '12312'

        request = Request.blank('/api/user/' + user_id + '/activate_with_id', method='POST')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

        global any_number
        self.assertEqual(user_id, any_number)

    @unittest.skip('skip')
    def test_action_with_shields(self):
        user_id = '123'
        request = Request.blank('/api/user/' + user_id + '/enable', method='POST')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

        global any_number
        self.assertEqual('enabled', any_number)

        user_id = '123'
        request = Request.blank('/api/user/' + user_id + '/enable_fail', method='POST')
        response = request.get_response(application)
        self.assertEqual(403, response.status_int)

    def test_action_url_404(self):
        request = Request.blank('/api/user/123/dontexists', method='POST')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)


@endpoint('/any')
class AnyModel(ModelInterface):
    pass

class ActionWrong(ActionAPI):

    @action("/activate")
    def activate(self):
        return False


class TestWrongCases(unittest.TestCase):

    def test_action_without_model(self):
        request = Request.blank('/api/any/123/activate', method='POST')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)
