
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

        raise exceptions.MethodNotFound()


class Shield(object):

    def __init__(self, info):
        self.info = info

    def get(cls):
        return True

    def delete(cls):
        return True

    def put(cls):
        return True

    def post(cls):
        return True
