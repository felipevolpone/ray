import webapp2
from handler.http_handler import ServiceRouter, AuthHandler

paths = [('/api/.*', ApiRouter)]
application = webapp2.WSGIApplication(paths)
