from . import exceptions, http
from .shield import ShieldHandler
from .application import ray_conf


def endpoint(url=None, authentication=None):
    def decorator(clazz):
        bla = url.replace('/', '')
        clazz._endpoint_url = bla
        ray_conf['endpoint'][bla] = {'model': clazz, 'authentication': authentication}

        return clazz
    return decorator


class EndpointHandler(object):

    def __init__(self, request, fullpath):
        self.__request = request
        self.__url = fullpath
        self.__endpoint_data = self.get_endpoint_data()

    def process(self):
        return EndpointProcessor(self.__request,
                                 self.__endpoint_data['model'],
                                 self.__user_data()).process()

    def get_endpoint_data(self):
        full_path = self.__url.split('/')
        model_url = full_path[-1] if len(full_path) == 3 else full_path[-2]

        return ray_conf['endpoint'][model_url]

    def is_protected(self):
        return self.get_endpoint_data()['authentication'] is not None

    def endpoint_authentication(self):
        return self.get_endpoint_data()['authentication']

    def __allowed(self):
        if not self.is_protected():
            return True

        if not 'Authentication' in self.__request.headers:
            return False

        return self.__endpoint_data['authentication'].is_loged(self.__request.headers['Authentication'])

    def __user_data(self):
        if not self.is_protected():
            return {}

        return self.__endpoint_data['authentication'].unpack_jwt(self.__request.headers['Authentication'])


class EndpointProcessor(object):

    def __init__(self, request, model, user_info):
        self.__request = request
        self.__model = model

        self.__shield_class = ShieldHandler(user_info).get_shield(model)

    def process(self):
        methods = {'post': self.__process_post, 'get': self.__process_get,
                   'put': self.__process_put, 'delete': self.__process_delete}
        http_verb = self.__request.method.lower()
        return methods[http_verb]()

    def __process_put(self):
        if hasattr(self.__request, 'logged_user') and not self.__shield_class.put(self.__request.logged_user):
            raise exceptions.MethodNotFound()

        id_param = http.get_id(self.__request.path)
        entity_json = self.__request.json
        if not id_param:
            exceptions.PutRequiresIdOnJson()

        entity_json['id'] = id_param
        entity = self.__model.to_instance(entity_json)
        return entity.update(entity_json).to_json()

    def __process_post(self):
        if not self.__shield_class.post(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        entity = self.__model.to_instance(self.__request.json)
        return entity.put().to_json()

    def __process_get(self):
        if not self.__shield_class.get(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        id_param = http.get_id(self.__request.path)
        params = http.query_params_to_dict(self.__request)

        try:
            if not id_param:
                return [model.to_json() for model in self.__model.find(**params)]

            return self._find_database(id_param).to_json()
        except:
            raise exceptions.ModelNotFound()

    def __process_delete(self):
        if not self.__shield_class.delete(self.__shield_class.info):
            raise exceptions.MethodNotFound()

        id_param = http.get_id(self.__request.path)
        try:
            return self._find_database(id_param).delete(id=id_param).to_json()

        except exceptions.HookException:
            raise exceptions.HookException()
        except:
            raise exceptions.ModelNotFound()

    def _find_database(self, id_param):
        model = self.__model.get(id=id_param)
        if not model:
            raise exceptions.ModelNotFound()

        return model
