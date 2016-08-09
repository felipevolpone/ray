from ray.model import Model
import uuid


def gen_uuid():
    return str(uuid.uuid4())


class ModelInterface(Model):

    def __init__(self, *a, **k):
        super(ModelInterface, self).__init__(*a, **k)
        self.id = None

    @classmethod
    def columns(cls):
        return cls.describe().keys()

    def put(self, *args, **kwargs):
        self.uuid = gen_uuid()
        return self

    @classmethod
    def get(cls, id=None):
        return cls()

    @classmethod
    def find(cls, *args, **kwargs):
        return [cls()]

    def delete(self, *args, **kwargs):
        return self
