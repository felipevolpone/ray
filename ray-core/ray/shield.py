
from . import exceptions


class ShieldHandler(object):

    def __init__(self, cookie_content):
        self.content = cookie_content

    def get_shield(self, model_class):

        for clazz in Shield.__subclasses__():
            if not hasattr(clazz, '__model__'):
                raise exceptions.ShieldDoNotHaveModel()

            if clazz.__model__ == model_class:
                return clazz(self.content)

        return Shield(self.content)


class Shield(object):

    def __init__(self, info):
        self.info = info

    def get(self, *args, **kwargs):
        return True

    def delete(self, *args, **kwargs):
        return True

    def put(self, *args, **kwargs):
        return True

    def post(self, *args, **kwargs):
        return True
