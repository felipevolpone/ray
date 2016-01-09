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

        print 'from_func', from_func

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

        print 'result', result
        return response.out.write(result)

    return inner


class ApiHandler(webapp2.RequestHandler):

    @to_json
    def dispatch(self):
        full_path = self.request.path.split('/')
        url_asked = full_path[-1]
        return self._get_class(url_asked)

    def _get_class(self, url_asked):
        module = importlib.import_module(OnHandsSettings.ENDPOINT_MODULES)

        for clazz_name in dir(module):
            item = getattr(module, clazz_name)
            try:
                item_called = item()
            except:
                continue

            if hasattr(item_called, '_yawpy_url'):
                url = getattr(item_called, '_yawpy_url')
                if url == url_asked:
                    return EndpointManager(self.request, self.response, item).process()

        return None

app = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
