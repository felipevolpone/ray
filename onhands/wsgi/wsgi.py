import webapp2
from onhands.api import ApiHandler

app = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
