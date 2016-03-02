
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
        user_json = auth_class.login(**login_json)
        cookie_name, cookie_value = auth_class.sign_cookie(user_json)
        return self.__response.set_cookie(cookie_name, cookie_value, path='/')
