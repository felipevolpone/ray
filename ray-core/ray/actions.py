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
        print cls
        print name
        print bases
        print methods
        print '\n'

        if '__model__' not in methods:  # to pass the ActionAPI class
            return type.__new__(cls, name, bases, methods)

        model_class = methods['__model__']
        for method_name, method in methods.items():
            if not method_name.startswith('__'):
                url = model_class._endpoint_url + '/' + method._action_url
                ray_conf['action'][url] = {'method': method, 'class_name': name}

        return type.__new__(cls, name, bases, methods)


class ActionAPI(object):
    __metaclass__ = RegisterActions

    def __init__(self, url):
        # url e.g: /api/user/123/action_name # TODO implement this case
        # url e.g: /api/user/action_name

        # action_url = http.param_at(url, -1)
        # model_id = http.param_at(url, 3)

        self.action_url = http.param_at(url, 1) + '/' + http.param_at(url, -1)
        self.__entire_url = url
        self.model_url = http.param_at(url, 2)

    def process_action(self, action_url, model_id):
        action_class = None

        method = ray_conf['action'][self.action_url]['method']
        action_class_name = ray_conf['action'][self.action_url]['class_name']

        for clazz in ActionAPI.__subclasses__():
            if not hasattr(clazz, '__model__'):
                raise exceptions.ActionDoNotHaveModel()

            if clazz.__name__ == action_class_name:
                action_class = clazz
                break

        return method(action_class(self.__entire_url), model_id)

        # if not action_class:
        #     raise exceptions.MethodNotFound()
        #
        # for methodname in action_class.__dict__:
        #     method = getattr(clazz(), methodname)
        #
        #     if hasattr(method, '_action_url') and action_url == method._action_url:
                # if hasattr(method, '_protection_shield_method') and self.__request:
                #     shield_method = method._protection_shield_method
                #
                #     cookie_content = http.get_cookie_content(self.__request)
                #     if not shield_method(cookie_content):
                #         raise exceptions.NotAuthorized()

                # return method(model_id)
#
        raise exceptions.MethodNotFound()
