
class Authentication(object):

    @classmethod
    def login(cls, username, password):

        user_json = cls.authenticate(username, password)
        if user_json:
            return user_json

        raise Exception

    @classmethod
    def authenticate(cls, username, password):
        raise NotImplementedError

    @classmethod
    def sign_cookie(cls, user_json):
        # remove password
        pass

    @classmethod
    def is_loged(cls, user_json):
        pass
