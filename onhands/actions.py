
def action(url):
    def dec(func):
        def inner(*arg, **kw):
            func(*arg, **kw)
        return inner
    return dec


class ActionAPI(object):
    pass
