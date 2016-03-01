
import json
from .authentication import Authentication


class LoginHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        auth_class = Authentication.__subclasses__()[0]

        login_json = json.loads(self.__request.body)
        user_json = auth_class._authentication_class.login(**login_json)
        cookie_name, cookie_value = auth_class.sign_cookie(user_json)
        return self.__response.set_cookie(cookie_name, cookie_value, path='/')

    def __is_protected(self):
        try:
            return (hasattr(self.__endpoint_class, '_authentication_class') and
                    self.__endpoint_class._authentication_class is not None)
        except:
            return False

    def __allowed(self):
        try:
            cookie = self.__request.cookies.get(authentication_helper._COOKIE_NAME)
            return self.__endpoint_class._authentication_class.is_loged(cookie)
        except:
            return False