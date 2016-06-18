
from ray.model import Model
from google.appengine.ext.ndb import Model as AppEngineModel
from google.appengine.ext import ndb


class GAEModel(AppEngineModel, Model):

    nome = ndb.StringProperty()

    @classmethod
    def columns(cls):
        return sorted(cls._properties.keys())

    def put(self):
        super(GAEModel, self).put()
        return AppEngineModel.put(self)
