
def action(url):
    def dec(func):
        def inner(*arg, **kw):
            func.__action_url = url.replace('/', '')
            return func(*arg, **kw)
        return inner
    return dec


class ActionAPI(object):

    @classmethod
    def get_action(self, url):
        pass
