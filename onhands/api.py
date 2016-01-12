import webapp2, json, importlib
from endpoint import EndpointManager


class OnHandsSettings(object):
    ENDPOINT_MODULES = ''
    ACTION_MODULES = ''


def to_json(fnc):
    def inner(*args, **kwargs):
        response = args[0].response
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        from_func = fnc(*args, **kwargs)

        result = json.dumps({'result': from_func})
        return response.out.write(result)

    return inner


class ApiHandler(webapp2.RequestHandler):

    @to_json
    def dispatch(self):
        full_path = self.request.path.split('/')
        url_asked = full_path[-1] if len(full_path) == 3 else full_path[-2]
        return self._get_class(url_asked)

    def _get_class(self, url_asked):
        module = importlib.import_module(OnHandsSettings.ENDPOINT_MODULES)

        for clazz_name in dir(module):
            item = getattr(module, clazz_name)
            try:
                item_called = item()
            except:
                continue

            if hasattr(item_called, '_onhands_url'):
                url = getattr(item_called, '_onhands_url')
                if url == url_asked:
                    return EndpointManager(self.request, self.response, item).process()

        self.response.status = 404

app = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
