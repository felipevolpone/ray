
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import sessionmaker
from ray.model import Model
from google.appengine.ext.ndb import Model as AppEngineModel
from google.appengine.ext import ndb


class GAEModel(Model, AppEngineModel):

    nome = ndb.StringProperty()

    def describe(self):
        pass

    @classmethod
    def columns(cls):
        return sorted(cls._properties.keys())
