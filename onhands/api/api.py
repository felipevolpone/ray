import webapp2
import importlib
from onhands import json_util
from endpoint import EndpointManager


class OnHandsSettings(object):
    ENDPOINT_MODULES = ''


def to_json(fnc):
    def inner(*args, **kwargs):
        response = args[0].response
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        from_func = fnc(*args, **kwargs)

        result = None
        if not from_func:
            result = {}

        elif isinstance(from_func, dict):
            result = json_util.from_json(from_func)
        elif isinstance(from_func, list):
            if len(from_func) > 0:
                if hasattr(from_func[0], 'to_json'):
                    from_func = {'result': [obj.to_json() for obj in from_func]}
                result = json_util.from_json(from_func)
        return response.out.write(result)

    return inner


class ApiHandler(webapp2.RequestHandler):

    @to_json
    def dispatch(self):
        full_path = self.request.path.split('/')
        module_name = full_path[-1]
        return self._get_class(module_name)

    def _get_class(self, module_name):
        module = importlib.import_module(OnHandsSettings.ENDPOINT_MODULES)

        for clazz_name in dir(module):
            clazz = getattr(module, clazz_name)
            if hasattr(clazz, '_yawpy_url'):
                url = getattr(clazz, '_yawpy_url')
                if url.replace('/', '') == module_name:
                    return EndpointManager(self.request, self.response, clazz).process()

        return None

app = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
