
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

    def find(self, *args, **kwargs):
        if not kwargs:
            return self.__class__.query().fetch()

        query = self.__class__.query()
        for field, value in kwargs.items():
            query = query.filter(getattr(self.__class__, field) == value)

        return query.fetch()

    def get(self, *args, **kwargs):
        return self.__class__.get_by_id(self.id)
