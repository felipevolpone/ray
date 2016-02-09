import webapp2


class Response(webapp2.Response):

    def __init__(self, json):
        self._json = json
        webapp2.Response.__init__(self)


def param_at(url, index):
    """
        index starts after the word after api.
        Example: /api/user/123, index 0 returns 123
        Example: /api/user/foo/123, index 0 returns foo, index 1 returns 123
    """
    params_after_base_url = url.split('/')[3:]
    if len(params_after_base_url) > index:
        return params_after_base_url[index]

    return None
