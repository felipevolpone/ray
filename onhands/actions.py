from functools import wraps


def action(url):
    def dec(func):
        func._action_url = url.replace('/', '')

        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)
        return inner
    return dec


class ActionAPI(object):

    @classmethod
    def get_action(cls, url, model, id_):
        url = url.replace('/', '')

        for clazz in cls.__subclasses__():
            for methodname in clazz.__dict__:
                try:
                    method = getattr(clazz(), methodname)
                    method(id_)
                except:
                    continue

                if hasattr(method, '_action_url'):
                    __action_url = method._action_url
                    if url == __action_url:
                        return methodname
