from . import exceptions, http, application
from .shield import ShieldHandler


def endpoint(url=None, authentication=None):
    def decorator(clazz):
        fixed_url = url.replace('/', '')
        clazz._endpoint_url = fixed_url
        application.add_endpoint(fixed_url, clazz, authentication)

        return clazz
    return decorator


class EndpointHandler(object):

    def __init__(self, request, fullpath):
        self.__request = request
        self.__url = fullpath
        self.__endpoint_data = self.get_endpoint_data()

    def process(self):
        logged_user = None

        if self.is_protected():
            logged_user = application.get_authentication().get_logged_user()
            if not logged_user:
                raise exceptions.NotAuthorized()

            self.__request.logged_user = logged_user

        return EndpointProcessor(self.__request, self.__endpoint_data['model'], logged_user).process()

    def get_endpoint_data(self):
        try:
            full_path = self.__url.split('/')
            model_url = full_path[-1] if len(full_path) == 3 else full_path[-2]
            return application.get_endpoint(model_url)
        except:
            raise exceptions.EndpointNotFound()

    def is_protected(self):
        return self.get_endpoint_data()['authentication'] is not None

    def endpoint_authentication(self):
        return self.get_endpoint_data()['authentication']


class EndpointProcessor(object):

    def __init__(self, request, model, user_data):
        self.__request = request
        self.__model = model
        self.__shield_class = ShieldHandler(user_data).get_shield(model)

    def process(self):
        methods = {'post': self.__process_post, 'get': self.__process_get,
                   'put': self.__process_put, 'delete': self.__process_delete}

        http_verb = self.__request.method.lower()
        return methods[http_verb]()

    def __process_put(self):
        self.__validate_shield('put')

        id_param = http.get_id(self.__request.path)
        entity_json = self.__request.json
        if not id_param:
            exceptions.PutRequiresIdOnJson()

        entity_json['id'] = id_param
        entity = self.__model.to_instance(entity_json)
        return entity.update(entity_json).to_json()

    def __process_post(self):
        self.__validate_shield('post')

        entity = self.__model.to_instance(self.__request.json)
        return entity.put().to_json(), 201

    def __process_get(self):
        self.__validate_shield('get')

        id_param = http.get_id(self.__request.path)
        params = http.query_params_to_dict(self.__request)

        if not id_param:
            return [model.to_json() for model in self.__model.find(**params)]

        return self.__find_database(id_param).to_json()

    def __process_delete(self):
        self.__validate_shield('delete')

        id_param = http.get_id(self.__request.path)
        try:
            return self.__find_database(id_param).delete(id=id_param).to_json()
        except exceptions.HookException:
            raise exceptions.HookException()

    def __find_database(self, id_param):
        model = self.__model.get(id=id_param)
        if not model:
            raise exceptions.ModelNotFound()

        return model

    def __validate_shield(self, shield_method_name):
        shield_method = getattr(self.__shield_class, shield_method_name)

        model_id = http.get_id(self.__request.path)
        parameters = http.get_parameters(self.__request)
        logged_user = self.__request.logged_user if hasattr(self.__request, 'logged_user') else None

        if logged_user and not shield_method(self.__request.logged_user, model_id, parameters):
            raise exceptions.MethodUnderShieldProtection()

        return True
