import webapp2, json
from endpoint import EndpointHandler
from login import LoginHandler
from actions import ActionAPI
from . import exceptions
from . import http


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

        try:
            return self.process(url)
        except exceptions.ModelNotFound:
            self.response.status = 404
        except exceptions.MethodNotFound:
            self.response.status = 404
        except exceptions.Forbidden:
            self.response.status = 403
        except exceptions.NotAuthorized:
            self.response.status = 403

    def __fix_url(self, url):
        if url[-1] == '/':
            return url[:-1]
        return url

    def process(self, fullpath):
        if self.is_login(fullpath):
            return (LoginHandler(self.request, self.response, fullpath)
                                .process())

        elif self.is_endpoint(fullpath):
            return EndpointHandler(self.request, self.response, fullpath).process()

        elif self.is_action(fullpath):
            return self.__handle_action(fullpath)
        else:
            self.response.status = 404

    def __handle_action(self, url):
        action_url = http.param_at(url, -1)
        model_name = http.param_at(url, 2)
        model_id = http.param_at(url, 3)
        return ActionAPI.get_action(model_name, action_url, model_id)

    def is_login(self, full_path):
        return full_path == '/api/login'

    def is_endpoint(self, full_path):
        return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2

    def is_action(self, full_path):
        return len(full_path.split('/')) == 5
