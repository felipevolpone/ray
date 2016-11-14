

class ShieldHandler(object):

    def __init__(self, user_data):
        self.user_data = user_data

    def get_shield(self, model_class):

        for clazz in Shield.__subclasses__():

            if clazz.__model__ == model_class:
                return clazz()

        # here an empty Shield is returned to avoid if is not None at the endpoint
        return Shield()


class Shield(object):
    """
        The Shield must be inherited if you want to protect some endpoint. Each method
        represents a http method (get, post, delete, etc), so just inherit that http
        method you wanna protect.

        See this example:
        class PersonShield(Shield):
            __model__ = PersonModel

            def get(self, user_data, model_id, parameters):
                return user_data['profile'] == 'admin'

        This way, the http request: GET /api/person/ will be under the protection of this method. This means that,
        if the property 'profile' in the cookie of the logged user is 'admin', the url will send an response. If This
        is no true, will send a 404.
        The info parameter in the get method is the response of the Authentication.authenticate method (a dict).
    """

    def get(self, user_data, model_id, parameters):
        return True

    def delete(self, user_data, model_id, parameters):
        return True

    def put(self, user_data, model_id, parameters):
        return True

    def post(self, user_data, model_id, parameters):
        return True
