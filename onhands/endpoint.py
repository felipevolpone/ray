from functools import wraps
from tests import storage
import json


def endpoint(url):
    def decorator(func):
        @wraps(func)
        def inner(*a, **k):
            func._endpoint_url = url.replace('/', '')
            return func(*a, **k)
        return inner
    return decorator


class EndpointManager(object):
    """
        EndpointManager handles with the request of a endpoint model.
        This will execute a method that is related with the http verb
        that it's correspond.
    """

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
        entity_json = json.loads(self.__request.body)
        entity = self.__model().__class__.to_instance(entity_json)
        return storage.put(entity).to_json()

    def __process_put(self):
        return self.__update_entity()

    def __process_post(self):
        return self.__update_entity()

    def __process_get(self):
        id_param = self.__request.param_at(0)
        if not id_param and not any(self.__request.params):
            return [model.to_json() for model in storage.find(self.__model())]

        return self._find_database()

    def __process_delete(self):
        id_param = self.__request.param_at(0)
        return storage.delete(self.__model(), id_param).to_json()

    def _find_database(self):
        id_param = self.__request.param_at(0)
        if id_param:
            model = storage.get(self.__model(), id_param)
            if not model:
                raise Exception('Model not found')
            return model.to_json()

        return [m.to_json() for m in storage.find(self.__model(), self.__request.params)]
