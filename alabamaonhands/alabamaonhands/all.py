from alabama.models import BaseModel, StringProperty
from alabama import storage
from alabama.connection import transaction
from onhands.model import Model
from onhands.api import ApiHandler
from onhands.api import to_json as req_json


class Api(ApiHandler):
   
    @req_json
    @transaction
    def dispatch(self):
        super(Api, self).dispatch()


class AlabamaModel(BaseModel, Model):
    
    # FIXME
    uuid = StringProperty()

    def __put(self):
        return storage.put(self)

    def __delete(self):
        return storage.delete(self, uuid=self.uuid)

    def put(self):
        succeed = super(AlabamaModel, self).put()
        if succeed:
            return self.__put()

    def delete(self):
        succeed = super(AlabamaModel, self).delete()
        if succeed:
            return self.__delete()

    def get(self, model_id):
        return storage.get(self, model_id)

AlabamaModel.find = storage.find

