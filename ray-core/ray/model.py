
from ray.exceptions import HookException


class Model(object):

    def __init__(self, *args, **kwargs):
        for k, value in kwargs.items():
            if k in dir(self):
                setattr(self, k, value)

    @classmethod
    def to_instance(cls, json):
        return cls(**json)

    def to_json(self):
        return_json = {}

        for field_name in sorted(self.columns()):
            value = getattr(self, field_name)
            if value:
                return_json[field_name] = value

        return return_json

    def describe(self):
        raise NotImplementedError

    @classmethod
    def columns(cls):
        raise NotImplementedError

    @classmethod
    def find(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get(cls, id=None):
        raise NotImplementedError

    def update(self, dict_fields_to_update):
        return self.__save()

    def put(self):
        return self.__save()

    def __save(self):
        if self._hasnt_hooks():
            return True

        for hook in self.hooks:
            instance = hook()

            # this is to make AND with the result of all hooks
            # the flow just continue if the result of all hoks is true

            try:
                if not instance.before_save(self):
                    raise Exception('The hook %s.before_save didnt return True' % (instance.__class__.__name__,))

            except NotImplementedError:
                continue

        return True

    def delete(self):
        if self._hasnt_hooks():
            return True

        for hook in self.hooks:
            instance = hook()

            # this is to make AND with the result of all hoks
            # the flow just continue if the result of all hoks is true
            try:
                if not instance.before_delete(self):
                    raise Exception('The hook %s.before_delete didnt return True' % (instance.__class__.__name__,))

            except NotImplementedError:
                continue

            except Exception:
                raise HookException('The hook %s.before_delete didnt return True' % (instance.__class__.__name__,))

        return True

    def _hasnt_hooks(self):
        return not hasattr(self, 'hooks')
