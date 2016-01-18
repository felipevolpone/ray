from alabama.models import BaseModel
from alabama import storage
from onhands.model import Model


class AlabamaModel(Model, BaseModel):

    def __put(self):
        return storage.put(self)

    def __delete(self):
        return storage.delete(self, self.uuid)

    def put(self):
        succeed = super(AlabamaModel, self).put()
        if succeed:
            return self.__put()

    def delete(self):
        succeed = super(AlabamaModel, self).delete()
        if succeed:
            return self.__delete()

