from functools import wraps
from . import exceptions


def action(url):
    def dec(func):
        func._action_url = url.replace('/', '')

        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)
        return inner
    return dec


class ActionAPI(object):

    @classmethod
    def get_action(cls, model_name, url, model_id):
        action_class = None
        for clazz in cls.__subclasses__():

            if not hasattr(clazz, '__model__'):
                raise exceptions.ActionDoNotHaveModel

            if clazz.__model__._endpoint_url == model_name:
                action_class = clazz
                break

        if not action_class:
            raise exceptions.MethodNotFound()

        for methodname in action_class.__dict__:
            method = getattr(clazz(), methodname)
            if hasattr(method, '_action_url') and url == method._action_url:
                return method(model_id)

        raise exceptions.MethodNotFound()
