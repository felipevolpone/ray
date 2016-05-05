import webapp2

from . import authentication_helper


class Response(webapp2.Response):

    def __init__(self, json):
        self._json = json
        webapp2.Response.__init__(self)


def param_at(url, index):
    """
        index starts after the word after api.
        Example: /api/user/123, index 3 returns 123
        Example: /api/user/foo/123, index 1 returns api, index 3 returns foo
    """
    if url and url[0] != '/':
        url = '/' + url

    params = url.split('/')
    if len(params) > index and index != 0:
        return params[index]

    return None


def get_id(url):
    return param_at(url, 3)


def get_cookie_content(request):
    cookie_text = request.cookies.get(authentication_helper._COOKIE_NAME)
    return authentication_helper.cookie_content(cookie_text)


def query_params_to_dict(get):
    params = {}
    for key, value in get.items():
        if isinstance(value, unicode):
            value = value.encode('UTF-8')

        params[key] = value

    return params
