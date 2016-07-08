import webapp2
from ray.api import ApiHandler

application = webapp2.WSGIApplication([('/api/.*', ApiHandler)], debug=True)
