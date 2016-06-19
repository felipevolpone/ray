
from ray.model import Model
from google.appengine.ext.ndb import Model as AppEngineModel


class GAEModel(AppEngineModel, Model):

    @classmethod
    def columns(cls):
        return sorted(cls._properties.keys())

    def put(self):
        super(GAEModel, self).put()
        return AppEngineModel.put(self)

    def remove(self, *args, **kwargs):
        super(AppEngineModel, self).delete()
        return self.key.delete()
