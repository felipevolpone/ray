from bottle import request as bottle_req, response as bottle_resp
from . import application
from datetime import datetime, timedelta


_COOKIE_NAME = 'RayAuth'


def _get_logged_user():
    token = bottle_req.get_cookie(_COOKIE_NAME)
    if not token:
        return None
    return application.get_authentication().unpack_jwt(token)


def _increase_cookie_timestamp():
    # FIXME
    cookie_data = _get_logged_user()
    timestamp = cookie_data['__expiration']
    new_timestamp = datetime.fromtimestamp(timestamp / 1000) + timedelta(minutes=5)
    cookie_data['__expiration'] = new_timestamp
    cookie_as_token = application.get_authentication().pack_jwt(cookie_data, application.get_authentication().salt_key)
    bottle_resp.set_cookie(_COOKIE_NAME, cookie_as_token.decode('utf-8'))


class LoginHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        auth_class = application.get_authentication()
        login_json = self.__request.json
        user_token = auth_class.login(login_json)
        self.__response.set_cookie(_COOKIE_NAME, user_token.decode('utf-8'))


class LogoutHandler(object):

    def __init__(self, response):
        self.__response = response

    def logout(self):
        self.__response.set_cookie(_COOKIE_NAME, '')
