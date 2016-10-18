
import jwt
from .exceptions import NotAuthorized
from .application import ray_conf


def register(clazz):
    ray_conf['authentication'] = clazz
    return clazz


class Authentication(object):

    @classmethod
    def login(cls, login_data):
        user_json = cls.authenticate(login_data)

        if not hasattr(cls, 'salt_key'):
            raise NotImplementedError()

        if user_json:
            return jwt.encode(user_json, cls.salt_key, algorithm='HS256')

        raise NotAuthorized()

    @classmethod
    def authenticate(cls, login_data):
        """ Here you can implement select in the database
            to garantee that the username and the password
            are from the same user. This method must return
            a dict
        """
        raise NotImplementedError()

    @classmethod
    def unpack_jwt(cls, token):
        if not hasattr(cls, 'salt_key'):
            raise NotImplementedError()

        return jwt.decode(token, cls.salt_key, algorithms=['HS256'])

    @classmethod
    def is_loged(cls, token):
        try:
            cls.unpack_jwt(token)
            return True
        except:
            return False
