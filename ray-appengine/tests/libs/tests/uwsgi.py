import webapp2


def create_application(app, paths):
    application = webapp2.WSGIApplication(paths)
