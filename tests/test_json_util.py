import unittest
from onhands import json_util
from onhands.endpoint import endpoint
from alabama.models import StringProperty, IntegerProperty, BaseModel


@endpoint('/user')
class UserModel(BaseModel):
    name = StringProperty()
    age = IntegerProperty()


class TestJson(unittest.TestCase):

    def test_from_list(self):
        persons = []
        for i in range(0, 2):
            persons.append(UserModel(name='felipe', age=i))

        persons_json = json_util.from_list(persons)
        self.assertEqual([{'name': 'felipe', 'age': 0, 'id': None},
                          {'name': 'felipe', 'age': 1, 'id': None}],
                         persons_json)
