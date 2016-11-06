
_ray_conf = {
    'endpoint': {},
    'action': {},
    'authentication': None
}


import logging

log = logging.getLogger('ray')
log.setLevel(logging.DEBUG)


def add_endpoint(url, modelclass, authentication):
    global _ray_conf
    _ray_conf['endpoint'][url] = {'model': modelclass, 'authentication': authentication}


def get_endpoint(model_url):
    global _ray_conf
    return _ray_conf['endpoint'][model_url]


def register_authentication(clazz):
    global _ray_conf
    _ray_conf['authentication'] = clazz


def get_authentication():
    global _ray_conf
    return _ray_conf['authentication']


def add_action(url, method, name):
    global _ray_conf
    _ray_conf['action'][url] = {'method': method, 'class_name': name}


def get_action_method(action_url):
    global _ray_conf
    return _ray_conf['action'][action_url]['method']


def get_action_class_name(action_url):
    global _ray_conf
    return _ray_conf['action'][action_url]['class_name']
