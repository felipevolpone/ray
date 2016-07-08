from functools import wraps
from . import exceptions, http
from .application import ray_conf


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


class RegisterActions(type):

    def __new__(cls, name, bases, methods):
        print name
        print methods
        print bases

        model_class = methods['__model__']
        for method_name, method in methods.items():
            if not method_name.startswith('__'):
                url = model_class._endpoint_url + '/' + method._action_url
                ray_conf[url] = method

        return type.__new__(cls, name, bases, methods)


class ActionAPI(object):
    __metaclass__ = RegisterActions

    def __init__(self, url):
        # url e.g: /api/user/123/action

        # action_url = http.param_at(url, -1)
        # model_id = http.param_at(url, 3)
        model_url = http.param_at(url, 2)
        self.__entire_url = url
        self.model_url = model_url

    def process_action(self, action_url, model_id):
        action_class = None

        for clazz in ActionAPI.__subclasses__():
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
                # if hasattr(method, '_protection_shield_method') and self.__request:
                #     shield_method = method._protection_shield_method
                #
                #     cookie_content = http.get_cookie_content(self.__request)
                #     if not shield_method(cookie_content):
                #         raise exceptions.NotAuthorized()

                return method(model_id)

        raise exceptions.MethodNotFound()
