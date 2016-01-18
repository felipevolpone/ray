
class Model(object):

    def __init__(self, *args, **kwargs):
        for k, value in kwargs.items():
            if k in self.__dict__:
                setattr(self, k, value)

    def put(self):
        if not hasattr(self, 'hooks'):
            return True 

        final_result = True
        for hook in self.hooks:
            instance = hook()

            # this is to make AND with the result of all hoks
            # the flow just continue if the result of all hoks is true
            try:
                if not instance.before_save(self):
                    final_result = False
                    break
            except NotImplementedError:
                continue

        if not final_result:
            raise Exception('The hook %s.before_save didnt return True' % (instance.__class__.__name__,))

        return True

    def delete(self):
        if not hasattr(self, 'hooks'):
            return True 

        final_result = True
        for hook in self.hooks:
            instance = hook()

            # this is to make AND with the result of all hoks
            # the flow just continue if the result of all hoks is true
            try:
                if not instance.before_delete(self):
                    final_result = False
                    break
            except NotImplementedError:
                continue
            
        if not final_result:
            raise Exception('The hook %s.before_delete didnt return True' % (instance.__class__.__name__,))

        return True

