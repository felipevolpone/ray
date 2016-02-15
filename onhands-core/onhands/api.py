import webapp2, json, importlib
from endpoint import EndpointManager
from actions import ActionAPI
from . import exceptions
from . import authentication_helper


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

        # is login
        if url.split('/')[-1] == 'login':
            return self._login(url)

        try:
            return self._get_class(url)
        except exceptions.ModelNotFound:
            self.response.status = 404
            return
        except exceptions.Forbidden:
            self.response.status = 403
            return

    def _login(self, url):
        login_json = json.loads(self.request.body)
        endpoint_clazz = self._get_endpoint_class(url)
        user_json = endpoint_clazz._authentication_class.login(**login_json)
        cookie_name, cookie_value = endpoint_clazz._authentication_class.sign_cookie(user_json)
        self.response.set_cookie(cookie_name, cookie_value, path='/')

    def __fix_url(self, url):
        if url[-1] == '/':
            return url[:-1]
        return url

    def _get_class(self, fullpath):
        if self.is_protected(fullpath) and not self._allowed():
            raise exceptions.Forbidden

        if self.is_endpoint(fullpath):
            return self.__handle_endpoint(fullpath)

        elif self.is_action(fullpath):
            return self.__handle_action(fullpath)

        else:
            self.response.status = 404

    def is_protected(self, url):
        try:
            endpoint_class = self._get_endpoint_class(url)
            return (hasattr(endpoint_class, '_authentication_class') and endpoint_class._authentication_class is not None)
        except:
            return False

    def _allowed(self):
        try:
            cookie = self.request.cookies.get(authentication_helper._COOKIE_NAME)
            return self._authentication_class.is_loged(cookie)
        except:
            return False

    def _get_endpoint_class(self, full_path):
        full_path = full_path.split('/')
        url_asked = full_path[-1] if len(full_path) == 3 else full_path[-2]
        module = importlib.import_module(OnHandsSettings.ENDPOINT_MODULES)

        for clazz_name in dir(module):
            model_clazz = getattr(module, clazz_name)
            if hasattr(model_clazz, '_endpoint_url'):
                if model_clazz._endpoint_url == url_asked:
                    return model_clazz

    def __call_enpodint(self, full_path):
        endpoint_class = self._get_endpoint_class(full_path)
        return EndpointManager(self.request, self.response, endpoint_class).process()

    def __handle_endpoint(self, full_path):
        return self.__call_enpodint(full_path)

    def __handle_action(self, url):
        splited = url.split('/')
        action_url = splited[-1].replace('/', '')
        model_id = splited[3]
        try:
            return ActionAPI.get_action(action_url, model_id)
        except:
            self.response.status = 404

    def is_endpoint(self, full_path):
        return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2

    def is_action(self, full_path):
        return len(full_path.split('/')) == 5
