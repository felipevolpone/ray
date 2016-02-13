
class Authentication(object):

    @classmethod
    def login(cls, username, password):
        user_json = cls.authenticate(username, password)
        if user_json:
            return user_json

        raise Exception

    @classmethod
    def authenticate(cls, username, password):
        """ Here you can implement select in the database
            to garantee that the username and the password
            are from the same user
        """
        raise NotImplementedError

    @classmethod
    def sign_cookie(cls, user_json):
        # remove password
        pass

    @classmethod
    def is_loged(cls, user_json):
        pass
