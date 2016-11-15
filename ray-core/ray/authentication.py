import jwt
from .exceptions import NotAuthorized, AuthenticationExpirationTime, Forbidden
from datetime import datetime, timedelta
from . import application, login


def register(clazz):
    application.register_authentication(clazz)
    return clazz


class Authentication(object):

    @classmethod
    def login(cls, login_data):
        user_json = cls.authenticate(login_data)

        if not hasattr(cls, 'salt_key'):
            raise NotImplementedError('You must define the salt_key method')
        else:
            try:
                cls.salt_key()
            except:
                raise NotImplementedError('You must define the salt_key method')

        if not hasattr(cls, 'expiration_time'):
            raise NotImplementedError('You must define the expiration_time')

        try:
            float(cls.expiration_time)
        except:
            raise AuthenticationExpirationTime('The expiration_time must be a integer')

        if user_json:
            return cls.keep_user_logged(user_json)

        raise Forbidden()

    @classmethod
    def keep_user_logged(cls, user_data):
        cls.__user_still_valid(user_data)

        if not '__expiration' in user_data:
            new_timestamp = datetime.now() + timedelta(minutes=cls.expiration_time)
        else:
            timestamp = int(user_data['__expiration'])
            new_timestamp = datetime.fromtimestamp(timestamp / 1000) + timedelta(minutes=cls.expiration_time)

        user_data['__expiration'] = int(new_timestamp.strftime('%s')) * 1000
        cookie_as_token = jwt.encode(user_data, cls.salt_key(), algorithm='HS256')
        return cookie_as_token

    @classmethod
    def __user_still_valid(cls, user_data):
        if '__expiration' not in user_data:
            return True

        timestamp = int(user_data['__expiration'])
        expiration_time = datetime.fromtimestamp(timestamp / 1000)
        now = datetime.now()

        if expiration_time < now:
            raise NotAuthorized()

        return True


    @classmethod
    def get_logged_user(cls):
        user_data = login._get_logged_user()
        if not user_data:
            return user_data

        if cls.__user_still_valid(user_data):
            del user_data['__expiration']
            return user_data

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
        return jwt.decode(token, cls.salt_key(), algorithms=['HS256'])
