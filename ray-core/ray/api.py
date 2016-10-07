import json, traceback, bottle
from bottle import request as bottle_req, response as bottle_resp
from .endpoint import EndpointHandler
from .login import LoginHandler, LogoutHandler
from .actions import ActionAPI
from . import exceptions, http
from functools import wraps

application = bottle.Bottle()


def to_json(fnc):
    @wraps(fnc)
    def inner(*args, **kwargs):
        bottle_resp.headers['Content-Type'] = 'application/json'
        from_func = fnc(*args, **kwargs)
        return json.dumps({'result': from_func})
    return inner


@application.route('/<url:re:.+>', method=['GET', 'POST', 'PUT', 'DELETE'], apply=to_json)
def dispatch(url):
    """
        This class is the beginning of all entrypoint in the Ray API. Here, each url
        will be redirect to the right handler: ActionHandler, LoginHandler or EndpointHandler.
    """
    url = bottle_req.path

    if url[-1] == '/':
        url = url[:-1]

    response_code = 200

    # FIXME each exception should contain there http response code
    # to do this create an class httpexception and all httpexception like this
    # bellow will inherit from it

    try:
        return process(url, bottle_req, bottle_resp)
    except (exceptions.MethodNotFound, exceptions.ActionDoNotHaveModel, exceptions.ModelNotFound) as e:
        response_code = 404
    except exceptions.BadRequest as e:
        response_code = 502
    except (exceptions.Forbidden, exceptions.NotAuthorized) as e:
        response_code = 403
    except exceptions.HookException:
        response_code = 400
    except Exception as e:
        response_code = 500
        traceback.print_exc()
    finally:
        bottle_resp.status = response_code


def process(fullpath, request, response):
    if is_login(fullpath):
        return LoginHandler(request, response, fullpath).process()

    if is_logout(fullpath):
        return LogoutHandler(response).logout()

    elif is_endpoint(fullpath):
        return EndpointHandler(request, fullpath).process()

    elif is_action(fullpath):
        return __handle_action(fullpath)

    else:
        raise exceptions.BadRequest()


def __handle_action(url):
    # url e.g: /api/user/123/action

    arg = None
    if len(url.split('/')) >= 5:  # indicate that has an id between endpoint and action_name
        arg = http.param_at(url, -2)

    return ActionAPI(url, arg, bottle_req).process_action()


def is_login(full_path):
    return full_path == '/api/_login'


def is_logout(full_path):
    return full_path == '/api/_logout'


def is_endpoint(full_path):
    full_path = full_path.split('?')[0]
    if len(full_path.split('/')) == 4:
        try:
            int(full_path.split('/')[-1])
            return True
        except:
            return False

    return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2


def is_action(full_path):
    # full_path e.g: /api/user/123/action
    # full_path e.g: /api/user/action

    if len(full_path.split('/')) >= 4:
        try:
            int(full_path.split('/')[-1])
        except:
            return True

    return len(full_path.split('/')) == 5
