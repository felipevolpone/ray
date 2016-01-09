import json
from functools import wraps
from alabama import storage


def endpoint(url):
    def decorator(func):
        @wraps(func)
        def inner(*a, **k):
            return func(*a, **k)
        inner._yawpy_url = url
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
        methods = {'post': self.__process_post, 'get': self.__process_get}
        http_verb = self.__request.method.lower()
        return methods[http_verb]()

    def __process_post(self):
        entity_json = json.loads(self.__request.body, encoding='utf-8')
        entity = self.__model().__class__.to_model(json=entity_json)
        entity.put()
        return entity.to_json()

    def __process_get(self):
        return [model.to_json() for model in storage.find(self.__model().__class__)]

    # TODO
    def __process_put(self):
        pass

    # TODO
    def __process_delet(self):
        pass
