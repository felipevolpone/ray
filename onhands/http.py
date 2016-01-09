import webapp2


class Response(webapp2.Response):

    def __init__(self, json):
        self._json = json
        webapp2.Response.__init__(self)
