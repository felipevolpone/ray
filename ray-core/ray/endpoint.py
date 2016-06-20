import json, http, importlib
from . import exceptions, authentication_helper
from .shield import ShieldHandler


class RaySettings(object):
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
        self.__endpoint_class = self._get_endpoint_class()

    def process(self):
        if self.__is_protected() and not self.__allowed():
            raise exceptions.MethodNotFound()

        return EndpointProcessor(self.__request,
                                 self.__response,
                                 self.__endpoint_class).process()

    def _get_endpoint_class(self):
        full_path = self.__url.split('/')
        url_asked = full_path[-1] if len(full_path) == 3 else full_path[-2]

        for module_name in RaySettings.ENDPOINT_MODULES:
            module = importlib.import_module(module_name)

            for clazz_name in dir(module):
                model_clazz = getattr(module, clazz_name)

                if (hasattr(model_clazz, '_endpoint_url') and model_clazz._endpoint_url == url_asked):
                    return model_clazz

    def __is_protected(self):
        try:
            return (hasattr(self.__endpoint_class, '_authentication_class')
                    and
                    self.__endpoint_class._authentication_class is not None)
        except:
            return False

    def __allowed(self):
        try:
            cookie = (self.__request
                          .cookies.get(authentication_helper._COOKIE_NAME))
            return self.__endpoint_class._authentication_class.is_loged(cookie)
        except:
            return False


class EndpointProcessor(object):

    def __init__(self, request, response, model):
        self.__request = request
        self.__response = response
        self.__model = model

        cookie_content = http.get_cookie_content(self.__request)
        self.__shield_class = ShieldHandler(cookie_content).get_shield(model)

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
        if not self.__shield_class.put(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        return self.__update_entity()

    def __process_post(self):
        if not self.__shield_class.post(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        return self.__update_entity()

    def __process_get(self):
        if not self.__shield_class.get(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        id_param = http.get_id(self.__request.upath_info)
        params = http.query_params_to_dict(self.__request.GET)
        try:
            if not id_param:
                return [model.to_json() for model in self.__model().find(**params)]

            return self._find_database(id_param)
        except:
            raise exceptions.ModelNotFound()

    def __process_delete(self):
        if not self.__shield_class.delete(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        id_param = http.get_id(self.__request.upath_info)
        try:
            return self.__model(id=id_param).delete().to_json()
        except:
            raise exceptions.ModelNotFound()

    def _find_database(self, id_param):
        model = self.__model.__class__.get(id=id_param)
        if not model:
            raise exceptions.ModelNotFound()

        return model.to_json()
