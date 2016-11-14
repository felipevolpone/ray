import json, bottle, logging
from bottle import request as bottle_req, response as bottle_resp

from .endpoint import EndpointHandler
from .login import LoginHandler, LogoutHandler, increase_cookie_timestamp
from .actions import Action
from . import exceptions, http
from functools import wraps


application = bottle.Bottle()
log = logging.getLogger('ray')


def to_json(fnc):
    @wraps(fnc)
    def inner(*args, **kwargs):
        bottle_resp.headers['Content-Type'] = 'application/json'
        from_func = fnc(*args, **kwargs)
        if from_func is not None:
            return json.dumps({'result': from_func})
    return inner


@application.route('/<url:re:.+>', method=['GET', 'POST', 'PUT', 'DELETE'], apply=to_json)
def dispatch(url):
    """
        This class is the beginning of all entrypoint in the Ray API. Here, each url
        will be redirect to the right handler: ActionHandler, LoginHandler or EndpointHandler.
    """

    url = bottle_req.path
    log.debug('request: %s', bottle_req.url)

    if url[-1] == '/':
        url = url[:-1]

    response_code = 200

    try:
        processed = process(url, bottle_req, bottle_resp)

        try:
            from_func, http_status = processed[0], processed[1]
            bottle_resp.status = http_status
            return from_func
        except:
            return processed

    except exceptions.RayException as e:
        log.exception('ray exception: ')
        response_code = e.http_code

    except:
        log.exception('exception:')
        raise

    bottle_resp.status = response_code


def process(fullpath, request, response):
    if __is_login(fullpath):
        return LoginHandler.process(request, response)

    elif __is_ping_status(fullpath):
        return _handle_ping_status()

    elif __is_logout(fullpath):
        return LogoutHandler.logout(response)

    elif _is_endpoint(fullpath):
        return EndpointHandler(request, fullpath).process()

    elif _is_action(fullpath):
        return __handle_action(fullpath), 200

    else:
        raise exceptions.BadRequest()


def _handle_ping_status():
    cookie_name, user_token = increase_cookie_timestamp()
    bottle_resp.set_cookie(cookie_name, user_token.decode('utf-8'))


def __handle_action(url):
    # url e.g: /api/user/123/action

    arg = None
    if len(url.split('/')) >= 5:  # indicate that has an id between endpoint and action_name
        arg = http.param_at(url, -2)

    return Action(url, arg, bottle_req).process_action()


def __is_ping_status(fullpath):
    return fullpath == '/api/_ping'


def __is_login(full_path):
    return full_path == '/api/_login'


def __is_logout(full_path):
    return full_path == '/api/_logout'


def _is_endpoint(full_path):
    full_path = full_path.split('?')[0]
    if len(full_path.split('/')) == 4:
        try:
            int(full_path.split('/')[-1])
            return True
        except:
            return False

    return len(full_path.split('/')) <= 4 and len(full_path.split('/')) > 2


def _is_action(full_path):
    # full_path e.g: /api/user/123/action
    # full_path e.g: /api/user/action

    if len(full_path.split('/')) >= 4:
        try:
            int(full_path.split('/')[-1])
        except Exception:
            return True

    return len(full_path.split('/')) == 5
