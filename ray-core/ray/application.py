
import logging, sys


_ray_conf = {
    'endpoint': {},
    'action': {},
    'authentication': None,
    'single_request': {}
}

# example
# {
#   "action": {
#     "notebook/#arg/deactivate": {
#       "class_name": "NotebookActions",
#       "method": <function NotebookActions.deactivate at 0x1033aed90>
#     },
#     "notebook/#arg/invite": {
#       "class_name": "NotebookActions",
#       "method": <function NotebookActions.invite_to_notebook at 0x1033a7f28>
#     }
#   },
#   "authentication": <class __main__.SimpleNoteAuthentication>,
#   "endpoint": {
#     "note": {
#       "authentication": <class __main__.SimpleNoteAuthentication>,
#       "model": <class __main__.Note>
#     },
#     "notebook": {
#       "authentication": <class __main__.SimpleNoteAuthentication>,
#       "model": <class __main__.Notebook>
#     }
#   },
#   "single_request": {"/api/status": {"class": <class __main__.SimpleNoteAuthentication>,
#                                      "authentication": Fale }
# }

log = logging.getLogger('ray')
__formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
__console_handler = logging.StreamHandler(sys.stdout)
__console_handler.setFormatter(__formatter)
log.addHandler(__console_handler)


def has_single_url(fullpath):
    for url, clazz in _ray_conf['single_request'].items():
        if url == fullpath:
            return True

    return False


def add_single_url(url, clazz, authentication):
    _ray_conf['single_request'][url] = {'class': clazz, 'authentication': authentication}


def get_single_url(url):
    return _ray_conf['single_request'].get(url)


def add_endpoint(url, modelclass, authentication):
    global _ray_conf
    _ray_conf['endpoint'][url] = {'model': modelclass, 'authentication': authentication}
    log.debug('adding a new Endpoint. url: %s, model endpoint: %s, has authentication: %s',
              url, modelclass, bool(authentication))


def get_endpoint(model_url):
    global _ray_conf
    endpoint = _ray_conf['endpoint'][model_url]
    log.debug('getting the Endpoint: %s', model_url)
    return endpoint


def register_authentication(clazz):
    global _ray_conf
    _ray_conf['authentication'] = clazz
    log.debug('registering the Authentication class: %s', clazz)


def get_authentication():
    global _ray_conf
    authentication = _ray_conf['authentication']
    log.debug('getting the Authentication class. which is %s', authentication)
    return authentication


def add_action(url, method, name):
    global _ray_conf
    _ray_conf['action'][url] = {'method': method, 'class_name': name}
    log.debug('adding a new Action. url: %s, method: %s, name: %s', url, method, name)


def get_action_method(action_url):
    global _ray_conf
    action_method = _ray_conf['action'][action_url]['method']
    log.debug('getting the action with the url: %s', action_url)
    return action_method


def get_action_class_name(action_url):
    global _ray_conf
    classname = _ray_conf['action'][action_url]['class_name']
    log.debug('getting the action class name with the url: %s', action_url)
    return classname
