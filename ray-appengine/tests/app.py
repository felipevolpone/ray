from ray.endpoint import endpoint, RaySettings
from ray_appengine.all import GAEModel
from google.appengine.ext import ndb
from ray.wsgi.wsgi import application


RaySettings.ENDPOINT_MODULES.append('app')


@endpoint('/user')
class User(GAEModel):

    name = ndb.StringProperty()
    age = ndb.IntegerProperty()

