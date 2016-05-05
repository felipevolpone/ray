from functools import wraps
from . import exceptions
import http


def action(url, protection=None):
    def dec(func):
        if protection:
            func._protection_shield_method = protection

        func._action_url = url.replace('/', '')

        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)
        return inner
    return dec


class ActionAPI(object):

    def __init__(self, model_name=None, request=None):
        self.model_name = model_name
        self.__request = request

    def process_action(self, action_url, model_id):
        action_class = None

        for clazz in self.__class__.__subclasses__():
            if not hasattr(clazz, '__model__'):
                raise exceptions.ActionDoNotHaveModel()

            if clazz.__model__._endpoint_url == self.model_name:
                action_class = clazz
                break

        if not action_class:
            raise exceptions.MethodNotFound()

        for methodname in action_class.__dict__:
            method = getattr(clazz(), methodname)

            if hasattr(method, '_action_url') and action_url == method._action_url:
                if hasattr(method, '_protection_shield_method') and self.__request:
                    shield_method = method._protection_shield_method

                    cookie_content = http.get_cookie_content(self.__request)
                    if not shield_method(cookie_content):
                        raise exceptions.NotAuthorized()

                return method(model_id)

        raise exceptions.MethodNotFound()
