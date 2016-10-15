import webapp2, json
from endpoint import EndpointHandler
from login import LoginHandler
from actions import ActionAPI
from . import exceptions, http


def to_json(fnc):
    def inner(*args, **kwargs):
        response = args[0].response
        response.headers['Content-Type'] = 'application/json'
        from_func = fnc(*args, **kwargs)

        result = json.dumps({'result': from_func})
        return response.out.write(result)

    return inner


class ApiHandler(webapp2.RequestHandler):
    """
        This class is the beginning of all entrypoint in the Ray API. Here, each url
        will be redirect to the right handler: ActionHandler, LoginHandler or EndpointHandler.
    """

    @to_json
    def dispatch(self):
        url = self.request.path
        if url[-1] == '/':
            url = url[:-1]

        response_code = 200

        # FIXME each exception should contain there http response code
        # to do this create an class httpexception and all httpexception like this
        # bellow will inherit from it

        try:
            return self.process(url)
        except (exceptions.MethodNotFound, exceptions.ActionDoNotHaveModel, exceptions.ModelNotFound) as e:
            response_code = 404
        except exceptions.BadRequest as e:
            response_code = 502
            print e
        except (exceptions.Forbidden, exceptions.NotAuthorized) as e:
            response_code = 403
            print e
        except exceptions.HookException:
            response_code = 400
        # except Exception as e:
        #     raise e
        else:
            response_code = 500
        finally:
            if response_code != 200:
                self.abort(response_code)

    def process(self, fullpath):
        if self.is_login(fullpath):
            return LoginHandler(self.request, self.response, fullpath).process()
        else
            if self.is_endpoint(fullpath):
                endpoint_handler = EndpointHandler(self.request, fullpath)
                if endpoint_handler.is_protected():
                    try
                        self.request.logged_user = endpoint_handler.endpoint_authentication().unpack_jwt(self.__request.headers['Authentication'])
                        return endpoint_handler.process()
                    except
                        self.response.status = 401
                else
                    return endpoint_handler.process()

            elif self.is_action(fullpath):
                return self.__handle_action(fullpath)

            else:
                self.response.status = 404

    def __handle_action(self, url):
        # url e.g: /api/user/123/action

        arg = None
        if len(url.split('/')) >= 5:  # indicatest that has an id between endpoint and action_name
            arg = http.param_at(url, -2)

        return ActionAPI(url, arg, self.request).process_action()

    def is_login(self, full_path):
        return full_path == '/api/_login'

    def is_endpoint(self, full_path):
        full_path = full_path.split('?')[0]
        if len(full_path.split('/')) == 4:
            try:
                int(full_path.split('/')[-1])
                return True
            except:
                return False

        return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2

    def is_action(self, full_path):
        # full_path e.g: /api/user/123/action
        # full_path e.g: /api/user/action

        if len(full_path.split('/')) >= 4:
            try:
                int(full_path.split('/')[-1])
            except:
                return True

        return len(full_path.split('/')) == 5

    def is_unprotected_endpoint(self, full_path):
       