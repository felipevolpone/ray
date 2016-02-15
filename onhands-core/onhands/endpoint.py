import json, http, importlib
from . import exceptions
from . import authentication_helper


class OnHandsSettings(object):
    ENDPOINT_MODULES = []


def endpoint(url=None, authentication=None):
    def decorator(clazz):
        clazz._endpoint_url = url.replace('/', '')
        clazz._authentication_class = authentication
        return clazz
    return decorator


class EndpointHandler(object):

    def __init__(self, request, response, fullpath):
        self.__response = response
        self.__request = request
        self.__url = fullpath

    def process(self):
        # is login
        if self.__url.split('/')[-1] == 'login':
            return self.__login()

        if self.__is_protected() and not self.__allowed():
            raise exceptions.Forbidden

        return self.__handle()

    def _get_endpoint_class(self):
        full_path = self.__url.split('/')
        url_asked = full_path[-1] if len(full_path) == 3 else full_path[-2]

        for module_name in OnHandsSettings.ENDPOINT_MODULES:
            module = importlib.import_module(module_name)
            for clazz_name in dir(module):
                model_clazz = getattr(module, clazz_name)
                if hasattr(model_clazz, '_endpoint_url') and model_clazz._endpoint_url == url_asked:
                        return model_clazz

    def __handle(self):
        endpoint_class = self._get_endpoint_class()
        return EndpointProcessor(self.__request, self.__response, endpoint_class).process()

    def __is_protected(self):
        try:
            endpoint_class = self._get_endpoint_class()
            return (hasattr(endpoint_class, '_authentication_class') and
                    endpoint_class._authentication_class is not None)
        except:
            return False

    def __allowed(self):
        try:
            cookie = self.__request.cookies.get(authentication_helper._COOKIE_NAME)
            return self._authentication_class.is_loged(cookie)
        except:
            return False

    def __login(self):
        login_json = json.loads(self.__request.body)
        endpoint_clazz = self._get_endpoint_class()
        user_json = endpoint_clazz._authentication_class.login(**login_json)
        cookie_name, cookie_value = endpoint_clazz._authentication_class.sign_cookie(user_json)
        self.__response.set_cookie(cookie_name, cookie_value, path='/')


class EndpointProcessor(object):

    def __init__(self, request, response, model):
        self.__request = request
        self.__response = response
        self.__model = model

    def process(self):
        methods = {'post': self.__process_post, 'get': self.__process_get,
                   'put': self.__process_put, 'delete': self.__process_delete}
        http_verb = self.__request.method.lower()
        return methods[http_verb]()

    def __update_entity(self):
        id_param = http.get_id(self.__request.upath_info)
        entity_json = json.loads(self.__request.body)
        if id_param:
            entity_json['id'] = id_param

        entity = self.__model.to_instance(entity_json)
        return entity.put().to_json()

    def __process_put(self):
        return self.__update_entity()

    def __process_post(self):
        return self.__update_entity()

    def __process_get(self):
        id_param = http.get_id(self.__request.upath_info)

        # TODO implement find with params
        try:
            if not id_param and not any(self.__request.params):
                return [model.to_json() for model in self.__model().find()]

            return self._find_database(id_param)
        except:
            raise exceptions.ModelNotFound()

    def __process_delete(self):
        id_param = http.get_id(self.__request.upath_info)
        try:
            return self.__model(id=id_param).delete().to_json()
        except:
            raise exceptions.ModelNotFound()

    def _find_database(self, id_param):
        if id_param:
            model = self.__model(id=id_param).get()
            if not model:
                raise exceptions.ModelNotFound()

            return model.to_json()

        # FIXME change self.__request.params to a dict
        return [m.to_json() for m in self.__model().find(self.__request.params)]
