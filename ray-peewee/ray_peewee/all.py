
from peewee import Model as PeeweeNativeModel
from ray.model import Model as RayModel


class PeeweeModel(PeeweeNativeModel, RayModel):

    def describe(self):
        raise NotImplementedError

    @classmethod
    def columns(cls):
        return sorted([c.name for c in cls._meta.sorted_fields])

    @classmethod
    def find(cls, *args, **kwargs):
        query = cls.select()
        for field, value in kwargs.items():
            query = query.where(getattr(cls, field) == value)

        return query

    @classmethod
    def get(cls, id=None):
        try:
            return super(PeeweeModel, cls).get(cls.id == int(id))
        except:
            return None

    def update(self, fields_to_update):
        model_id = fields_to_update['id']
        del fields_to_update['id']

        model_class = self.__class__

        query = super(PeeweeModel, self).update(**fields_to_update)
        query = query.where(model_class.id == model_id)
        query.execute()

        for field, value in fields_to_update.items():
            setattr(self, field, value)

        return self

    def put(self):
        super(PeeweeModel, self).put()
        can_save = RayModel.put(self)
        if can_save:
            self.save()
            return self

    def delete(self, id=None):
        can_delete = RayModel.delete(self)
        if can_delete:
            query = super(PeeweeModel, self).delete().where(self.__class__.id == id)
            query.execute()
            return self

