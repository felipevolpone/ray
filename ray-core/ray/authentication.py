import jwt
from .exceptions import NotAuthorized
from datetime import datetime
from . import application, login


def register(clazz):
    application.register_authentication(clazz)
    return clazz


class Authentication(object):

    @classmethod
    def login(cls, login_data):
        user_json = cls.authenticate(login_data)

        if not hasattr(cls, 'salt_key'):
            raise NotImplementedError('You must define the salt_key')

        if user_json:
            return Authentication.pack_jwt(user_json, cls.salt_key)

        raise NotAuthorized()

    @classmethod
    def get_logged_user(cls):
        return login._get_logged_user()

    @classmethod
    def pack_jwt(cls, user_json, salt_key):
        user_json['__expiration'] = int(datetime.now().strftime('%s')) * 1000
        return jwt.encode(user_json, salt_key, algorithm='HS256')

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
            raise NotImplementedError('You must define the salt_key')

        return jwt.decode(token, cls.salt_key, algorithms=['HS256'])

    @classmethod
    def is_loged(cls, token):
        try:
            cls.unpack_jwt(token)
            return True
        except:
            return False
