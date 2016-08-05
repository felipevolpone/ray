import webapp2, urlparse

from . import authentication_helper


class Response(webapp2.Response):

    def __init__(self, json):
        self._json = json
        webapp2.Response.__init__(self)


def param_at(url, index):
    """
        index starts after the word after api.
        Example: /api/user/123, index 2 returns 123
        Example: /api/user/foo/123, index 1 returns user, index 2 returns foo
    """
    if url and url[0] == '/':
        url = url[1:]

    url = url.replace('api/', '')

    if index > 0:
        index -= 1
    elif index == 0:
        return None

    params = url.split('/')
    if len(params) > index:
        return params[index]

    return None


def get_id(url):
    return param_at(url, 2)


def get_cookie_content(request):
    cookie_text = request.cookies.get(authentication_helper._COOKIE_NAME)
    return authentication_helper.cookie_content(cookie_text)


def query_params_to_dict(request):
    params_with_array = urlparse.parse_qs(request.query_string)
    params = {}
    for key, values in params_with_array.items():
        value = values[0]
        try:
            value = int(values[0])
        except:
            pass
        params[key] = value

    return params
