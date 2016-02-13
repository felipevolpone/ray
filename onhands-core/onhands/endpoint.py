import json, http
from . import exceptions


def endpoint(url):
    def decorator(clazz):
        clazz._endpoint_url = url.replace('/', '')
        return clazz
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
        entity = self.__model.to_instance(entity_json)
        return entity.put().to_json()

    def __process_put(self):
        return self.__update_entity()

    def __process_post(self):
        return self.__update_entity()

    def __process_get(self):
        id_param = http.param_at(self.__request.upath_info, 0)

        # TODO implement find with params
        if not id_param and not any(self.__request.params):
            return [model.to_json() for model in self.__model().find()]

        return self._find_database(id_param)

    def __process_delete(self):
        id_param = http.param_at(self.__request.upath_info, 0)
        return self.__model(id=id_param).delete().to_json()

    def _find_database(self, id_param):
        if id_param:
            model = self.__model(id=id_param).get()
            if not model:
                raise exceptions.ModelNotFound()

            return model.to_json()

        # FIXME change self.__request.params to a dict
        return [m.to_json() for m in self.__model().find(self.__request.params)]
