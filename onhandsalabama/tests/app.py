import unittest
from alabama import connection
from onhandsalabama.all import AlabamaModel
from alabama.models import StringProperty, IntegerProperty
from onhands.endpoint import endpoint
from onhands.wsgi.wsgi import application


@endpoint('/user')
class User(AlabamaModel):
    name = StringProperty()
    age = IntegerProperty()
