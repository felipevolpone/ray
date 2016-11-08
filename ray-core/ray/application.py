
import logging, sys


_ray_conf = {
    'endpoint': {},
    'action': {},
    'authentication': None
}

log = logging.getLogger('ray')
__formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
__console_handler = logging.StreamHandler(sys.stdout)
__console_handler.setFormatter(__formatter)
log.addHandler(__console_handler)


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
