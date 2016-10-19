from ray.model import Model
import random


def gen_uuid():
    return random.randint(0, 1000000)


class ModelInterface(Model):

    def __init__(self, *a, **k):
        super(ModelInterface, self).__init__(*a, **k)
        self.id = None

    def put(self, *args, **kwargs):
        self.id = gen_uuid()
        return self

    @classmethod
    def get(cls, id=None):
        return cls()

    @classmethod
    def find(cls, *args, **kwargs):
        return [cls()]

    def delete(self, *args, **kwargs):
        return self

    def update(self, *args, **kwargs):
        return self
