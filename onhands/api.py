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
        url = self.__fix_url(self.request.path)
        return self._get_class(url)

    def __fix_url(self, url):
        if url[-1] == '/':
            return url[:-1]
        return url

    def handle_endpoint(self, full_path):
        full_path = full_path.split('/')
        url_asked = full_path[-1] if len(full_path) == 3 else full_path[-2]
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

    def is_endpoint(self, full_path):
        return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2

    def is_action(self, full_path):
        return len(full_path.split('/')) == 5

    def _get_class(self, fullpath):
        if self.is_endpoint(fullpath):
            return self.handle_endpoint(fullpath)
        elif self.is_action(fullpath):
            return self.handle_action(fullpath)
        else:
            self.response.status = 404

app = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
