from ray.endpoint import endpoint, RaySettings
from ray_appengine.all import GAEModel
from google.appengine.ext import ndb
from ray.wsgi.wsgi import application


RaySettings.ENDPOINT_MODULES.append('app')


@endpoint('/user')
class User(AlchemyModel, Base):
    __tablename__ = 'tb_user'
    __engine__ = engine

    name = ndb.StringProperty()
    age = ndb.IntegerProperty()

