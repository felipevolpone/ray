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
any_data = None


class UserShield(Shield):
    __model__ = UserModel

    @staticmethod
    def protect_enable(info):
        return True

    @staticmethod
    def protect_fail(info):
        return False


class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("/activate")
    def activate_user(self, model_id, parameters):
        # just to make sure that this method was called
        global any_number
        any_number = 'ACTIVATE_USER'
        return 'activate_user'

    @action("/<id>/activate_with_id")
    def activate_user_with_id(self, model_id, parameters):
        # just to make sure that this method was called
        global any_number
        any_number = model_id
        return 'activate_user_with_id'

    # to test Shileds with Actions
    @action('/enable', protection=UserShield.protect_enable)
    def enable_user(self, model_id, parameters):
        global any_number
        any_number = 'enabled'

    @action('/enable_fail', protection=UserShield.protect_fail)
    def enable_fail(self, model_id, parameters):
        pass

    @action('/test_parameters')
    def test_parameters(self, model_id, parameters):
        global any_data
        any_data = parameters


class TestAction(unittest.TestCase):

    def test_action(self):
        request = Request.blank('/api/user/activate', method='POST')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)
        global any_number
        self.assertEqual('ACTIVATE_USER', any_number)

        user_id = '12312'
        request = Request.blank('/api/user/' + user_id + '/activate_with_id', method='POST')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

        global any_number
        self.assertEqual(user_id, any_number)

    def test_action_with_shields(self):
        request = Request.blank('/api/user/enable', method='POST')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

        global any_number
        self.assertEqual('enabled', any_number)

        request = Request.blank('/api/user/enable_fail', method='POST')
        response = request.get_response(application)
        self.assertEqual(403, response.status_int)

    def test_action_url_404(self):
        request = Request.blank('/api/user/123/dontexists', method='POST')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)

    def test_action_parameters(self):
        params = 'user_id=10&age=3&name=felipe'
        request = Request.blank('/api/user/test_parameters?' + params, method='GET')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)
        global any_data
        self.assertEqual({'user_id': '10', 'age': '3', 'name': 'felipe'}, any_data)

        request = Request.blank('/api/user/test_parameters', method='POST')
        request.json = {'user_id': '10', 'age': '3', 'name': 'felipe'}
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)
        global any_data
        self.assertEqual({'user_id': '10', 'age': '3', 'name': 'felipe'}, any_data)


@endpoint('/any')
class AnyModel(ModelInterface):
    pass


class ActionWrong(ActionAPI):

    @action("/activate")
    def activate(self, parameters):
        return False


class TestWrongCases(unittest.TestCase):

    def test_action_without_model(self):
        request = Request.blank('/api/any/123/activate', method='POST')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)
