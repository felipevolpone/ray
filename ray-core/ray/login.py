
import json
from .authentication import Authentication


class LoginHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        auth_class = Authentication.__subclasses__()[-1]
        login_json = json.loads(self.__request.body)
        user_token = auth_class.login(login_json)
        return user_token


class LogoutHandler(object):

    def __init__(self, response):
        self.__response = response

    def logout(self):
        # self.__response.set_cookie(authentication_helper._COOKIE_NAME, '', path='/', expires=0)
        return True
