
from . import application
from .exceptions import BadRequest


def api(url, authentication=False):
    def decorator(clazz):
        fixed_url = url.replace('/', '')
        fixed_url = '/api/' + fixed_url
        clazz._single_url = fixed_url
        application.add_single_url(fixed_url, clazz, authentication)
        return clazz
    return decorator


class Request(object):

    def get(self, request, response):
        raise NotImplementedError()

    def put(self, request, response):
        raise NotImplementedError()

    def post(self, request, response):
        raise NotImplementedError()

    def delete(self, request, response):
        raise NotImplementedError()


class SingleRequestHandler(object):

    @classmethod
    def process(cls, fullpath, http_method, request, response):
        single_request = application.get_single_url(fullpath)

        if not single_request:
            raise BadRequest()

        clazz, has_auth = single_request['class'], single_request['authentication']
        instance = clazz()

        # TODO check authentication
        return getattr(instance, http_method)(request, response)
