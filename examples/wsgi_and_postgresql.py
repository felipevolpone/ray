
from onhands.endpoint import endpoint
from alabamaonhands.models import AlabamaModel
from alabama.models import StringProperty, IntegerProperty


@endpoint('/user')
class User(AlabamaModel):
    name = StringProperty()
    lastname = StringProperty()
    age = IntegerProperty()

