from functools import wraps
from . import exceptions, http, application
from future.utils import with_metaclass
import re


def action(url, protection=None, authentication=False):
    # url e.g: /<id>/action_name

    def dec(func):
        if protection:
            func._protection_shield_method = protection

        if authentication:
            func._action_under_authentication = True

        edit_url = url
        if edit_url.startswith('/'):  # remove the first /
            edit_url = edit_url[1:]

        pattern = re.search(r'\<(.*?)\>', url)
        if pattern:
            edit_url = edit_url.replace(pattern.group(), '#arg')

        func._action_url = edit_url

        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)
        return inner

    return dec


class RegisterActions(type):

    def __new__(cls, name, bases, methods):

        if '__model__' not in methods:  # to pass the Action class
            return type.__new__(cls, name, bases, methods)

        model_class = methods['__model__']
        for method_name, method in methods.items():
            if not method_name.startswith('__'):
                url = model_class._endpoint_url + '/' + method._action_url
                application.add_action(url, method, name)

        return type.__new__(cls, name, bases, methods)


class Action(with_metaclass(RegisterActions)):

    def __init__(self, url=None, model_arg=None, request=None):
        # url e.g: /api/user/123/action_name
        # url e.g: /api/user/action_name

        self.__request = request

        if not model_arg:
            self.action_url = http.param_at(url, 1) + '/' + http.param_at(url, -1)  # e.g: 'user/action_name'
        else:
            self.action_url = http.param_at(url, 1) + '/#arg/' + http.param_at(url, -1)  # e.g: 'user/123/action_name'

        self.__model_arg = model_arg
        self.__entire_url = url

    def process_action(self):
        action_class = None

        method = None
        try:
            method = application.get_action_method(self.action_url)
        except:
            raise exceptions.MethodNotFound()

        action_class_name = application.get_action_class_name(self.action_url)

        for clazz in Action.__subclasses__():

            if clazz.__name__ == action_class_name:
                action_class = clazz
                break

        authentication_class = application.get_authentication()
        request_parameters = http.get_parameters(self.__request)

        user_data = None
        if authentication_class:
            user_data = authentication_class.get_logged_user()

        if hasattr(method, '_protection_shield_method'):
            shield_method = method._protection_shield_method

            if not shield_method(user_data, self.__model_arg, request_parameters):  # shield returned False FIXME(improve tests)
                raise exceptions.NotAuthorized()

        if hasattr(method, '_action_under_authentication'):
            if not user_data:
                raise exceptions.ActionUnderAuthenticationProtection()

        request_parameters = http.get_parameters(self.__request)
        return method(action_class(self.__entire_url, None, self.__request), self.__model_arg, request_parameters)
