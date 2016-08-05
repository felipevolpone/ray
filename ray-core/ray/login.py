
import json
from .authentication import Authentication
from . import authentication_helper


class LoginHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        auth_class = Authentication.__subclasses__()[-1]

        login_json = json.loads(self.__request.body)
        user_json = auth_class.login(**login_json)
        cookie_name, cookie_value = auth_class.sign_cookie(user_json)
        self.__response.set_cookie(cookie_name, cookie_value, path='/')
        return True


class LogoutHandler(object):

    def __init__(self, response):
        self.__response = response

    def logout(self):
        self.__response.set_cookie(authentication_helper._COOKIE_NAME, None, path='/')
        return True
