import webapp2, json, importlib
from endpoint import EndpointManager
from actions import ActionAPI


class OnHandsSettings(object):
    ENDPOINT_MODULES = ''


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

    def __handle_endpoint(self, full_path):
        full_path = full_path.split('/')
        url_asked = full_path[-1] if len(full_path) == 3 else full_path[-2]
        module = importlib.import_module(OnHandsSettings.ENDPOINT_MODULES)

        for clazz_name in dir(module):
            item_called = getattr(module, clazz_name)
            if hasattr(item_called, '_endpoint_url'):
                url = getattr(item_called, '_endpoint_url')
                if url == url_asked:
                    return EndpointManager(self.request, self.response, item_called).process()

    def __handle_action(self, url):
        splited = url.split('/')
        action_url = splited[-1].replace('/','')
        model_id = splited[3]
        return ActionAPI.get_action(action_url, model_id)

    def is_endpoint(self, full_path):
        return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2

    def is_action(self, full_path):
        return len(full_path.split('/')) == 5

    def _get_class(self, fullpath):
        if self.is_endpoint(fullpath):
            return self.__handle_endpoint(fullpath)
        elif self.is_action(fullpath):
            return self.__handle_action(fullpath)
        else:
            self.response.status = 404

app = webapp2.WSGIApplication([('/api/.*', ApiHandler)])
