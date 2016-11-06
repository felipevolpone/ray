
ray_conf = {
    'endpoint': {},
    'action': {},
    'authentication': None
}


import logging

log = logging.getLogger('ray')
log.setLevel(logging.DEBUG)
# frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log.setFormatter(frmt)


def add_endpoint(url, modelclass, authentication):
    global ray_conf
    ray_conf['endpoint'][url] = {'model': modelclass, 'authentication': authentication}


def get_endpoint(model_url):
    global ray_conf
    return ray_conf['endpoint'][model_url]


def register_authentication(clazz):
    global ray_conf
    ray_conf['authentication'] = clazz


def get_authentication():
    global ray_conf
    return ray_conf['authentication']


def add_action(url, method, name):
    global ray_conf
    ray_conf['action'][url] = {'method': method, 'class_name': name}


def get_action_method(action_url):
    global ray_conf
    return ray_conf['action'][action_url]['method']


def get_action_class_name(action_url):
    global ray_conf
    return ray_conf['action'][action_url]['class_name']
