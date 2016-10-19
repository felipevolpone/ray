
from .application import ray_conf


class LoginHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        auth_class = ray_conf['authentication']
        login_json = self.__request.json
        user_token = auth_class.login(login_json)
        return {'token': user_token.decode('utf-8')}


class LogoutHandler(object):

    def __init__(self, response):
        self.__response = response

    def logout(self):
        # self.__response.set_cookie(authentication_helper._COOKIE_NAME, '', path='/', expires=0)
        # FIXME using jwt there is no logout, but the invalidation of the token in the login
        # each token should have a timestamp to expire
        return True
