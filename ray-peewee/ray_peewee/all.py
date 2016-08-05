
import peewee
from ray.model import Model


class PeeweeModel(peewee.Model, Model):

    def describe(self):
        raise NotImplementedError

    @classmethod
    def columns(cls):
        return sorted([c.name for c in cls._meta.sorted_fields])

    @classmethod
    def find(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get(cls, id=None):
        raise NotImplementedError
