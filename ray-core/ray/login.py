
from .application import ray_conf


_COOKIE_NAME = 'RayAuth'


def get_authenticated_user(request):
    token = request.get_cookie(_COOKIE_NAME)
    if not token:
        return None
    return ray_conf['authentication'].unpack_jwt(token)


class LoginHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        auth_class = ray_conf['authentication']
        login_json = self.__request.json
        user_token = auth_class.login(login_json)
        self.__response.set_cookie(_COOKIE_NAME, user_token.decode('utf-8'))


class LogoutHandler(object):

    def __init__(self, response):
        self.__response = response

    def logout(self):
        self.__response.set_cookie(_COOKIE_NAME, '')
