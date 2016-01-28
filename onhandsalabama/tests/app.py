import unittest
from alabama import connection
from onhandsalabama.all import AlabamaModel
from alabama.models import StringProperty, IntegerProperty
from onhands.endpoint import endpoint


@endpoint('/user')
class User(AlabamaModel):
    name = StringProperty()
    age = IntegerProperty()
