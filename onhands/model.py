from alabama.models import BaseModel
from alabama import storage


class Model(BaseModel):

    def __put(self):
        return storage.put(self)

    def __delete(self):
        return storage.delete(self, self.uuid)

    def put(self):
        if not hasattr(self, 'hooks'):
            return self.__put()

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

        if final_result:
            return self.__put()

        raise Exception('The hook %s.before_save didnt return True' % (instance.__class__.__name__,))

    def delete(self):
        if not hasattr(self, 'hooks'):
            return self.__delete()

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
            
        if final_result:
            return self.__delete()

        raise Exception('The hook %s.before_delete didnt return True' % (instance.__class__.__name__,))
