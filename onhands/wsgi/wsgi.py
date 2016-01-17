import webapp2
from onhands.api import ApiHandler

application = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
