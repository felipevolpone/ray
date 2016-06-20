
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

    @classmethod
    def find(cls, *args, **kwargs):
        query = cls.query()

        if not kwargs:
            return [entity.to_dict() for entity in query.fetch()]

        for field, value in kwargs.items():
            query = query.filter(getattr(cls, field) == value)

        return [entity.to_dict() for entity in query.fetch()]

    @classmethod
    def get(cls, id=None):
        return cls.get_by_id(id)
