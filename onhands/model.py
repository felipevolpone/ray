from alabama.models import BaseModel
from alabama import storage


class Model(BaseModel):

    def __put(self):
        return storage.put(self)

    def put(self):
        if not hasattr(self, 'hooks'):
            return self.__put()

        final_result = True
        for hook in self.hooks:
            instance = hook()

            # this is to make AND with the result of all hoks
            # the flow just continue if the result of all hoks is true
            if not instance.pre_save(self):
                final_result = False
                break

        if final_result:
            return self.__put()

        raise Exception('The hook %s.pre_save didnt return True' % (instance.__class__.__name__,))
