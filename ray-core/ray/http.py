import webapp2


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
