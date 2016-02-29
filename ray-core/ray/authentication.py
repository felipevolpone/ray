
import base64
from . import authentication_helper
from exceptions import NotAuthorized


class Authentication(object):

    @classmethod
    def login(cls, username, password):
        user_json = cls.authenticate(username, password)
        if user_json:
            return user_json

        raise NotAuthorized

    @classmethod
    def authenticate(cls, username, password):
        """ Here you can implement select in the database
            to garantee that the username and the password
            are from the same user. This method must return
            a dict
        """
        raise NotImplementedError

    @classmethod
    def sign_cookie(cls, user_json):
        cookie_name, cookie_value = authentication_helper.sign_cookie(user_json)
        return cookie_name, base64.b64encode(cookie_value)

    @classmethod
    def is_loged(cls, cookie_value):
        return authentication_helper._validate(cookie_value)
