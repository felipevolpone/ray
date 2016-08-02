
from . import exceptions


class ShieldHandler(object):

    def __init__(self, cookie_content):
        self.content = cookie_content

    def get_shield(self, model_class):

        for clazz in Shield.__subclasses__():
            if not hasattr(clazz, '__model__'):
                raise exceptions.ShieldDoNotHaveModel()

            if clazz.__model__ == model_class:
                return clazz(self.content)

        return Shield(self.content)  # here an empty Shield is returned to avoid if is not None at the endpoint


class Shield(object):
    """
        The Shiled must be inherited if you want to protect some endpoint. Each method
        represents a http method (get, post, delete, etc), so just inherit that http
        method you wanna protect.

        See this example:
        class PersonShield(Shield):
            __model__ = PersonModel

            def get(self, info):
                return info['profile'] == 'admin'

        This way, the http request: GET /api/person/ will be under the protection of this method. This means that,
        if the property 'profile' in the cookie of the logged user is 'admin', the url will send an response. If This
        is no true, will send a 404.
        The info parameter in the get method is the response of the Authentication.authenticate method (a dict).
    """

    def __init__(self, info):
        self.info = info

    def get(self, *args, **kwargs):
        return True

    def delete(self, *args, **kwargs):
        return True

    def put(self, *args, **kwargs):
        return True

    def post(self, *args, **kwargs):
        return True
