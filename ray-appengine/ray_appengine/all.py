
from ray.model import Model
from google.appengine.ext.ndb import Model as AppEngineModel
from google.appengine.ext import ndb


class GAEModel(AppEngineModel, Model):

    @classmethod
    def columns(cls):
        return sorted(cls._properties.keys())

    @classmethod
    def to_instance(cls, json_attributes):
        # instance = cls(**json_attributes)
        instance = cls()

        keys = {}
        for name, property_type in instance._properties.items():
            if isinstance(property_type, ndb.KeyProperty):
                keys[name] = property_type._kind

        for field_name in json_attributes.keys():
            value = json_attributes[field_name]
            if field_name in keys:
                value = ndb.Key(keys[field_name], json_attributes[field_name])

            setattr(instance, field_name, value)

        return instance

    def put(self):
        can_save = Model.put(self)
        if can_save:
            AppEngineModel.put(self)
            return self

    def remove(self, *args, **kwargs):
        can_delete = Model.delete(self)
        if can_delete:
            super(AppEngineModel, self).delete()
            return self.key.delete()

    def to_json(self):
        r = self.to_dict()
        if self.key:
            r['id'] = self.key.id()

        return r

    @classmethod
    def find(cls, *args, **kwargs):
        query = cls.query()

        if not kwargs:
            return query.fetch()

        for field, value in kwargs.items():
            query = query.filter(getattr(cls, field) == value)

        return query.fetch()

    @classmethod
    def get(cls, id=None):
        return cls.get_by_id(id)
