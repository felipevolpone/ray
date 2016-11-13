from bottle import request as bottle_req
from . import application


_COOKIE_NAME = 'RayAuth'


def _get_logged_user():
    token = bottle_req.get_cookie(_COOKIE_NAME)
    if not token:
        return None
    return application.get_authentication().unpack_jwt(token)


def increase_cookie_timestamp():
    authentication_class = application.get_authentication()
    user_token = authentication_class.keep_user_logged(_get_logged_user())
    return _COOKIE_NAME, user_token


class LoginHandler(object):

    @classmethod
    def process(self, request, response):
        auth_class = application.get_authentication()
        user_token = auth_class.login(request.json)
        response.set_cookie(_COOKIE_NAME, user_token.decode('utf-8'))


class LogoutHandler(object):

    @classmethod
    def logout(self, response):
        response.set_cookie(_COOKIE_NAME, '')
