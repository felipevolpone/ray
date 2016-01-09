import unittest
from util import json_util
from tests.mock import Person


class TestJson(unittest.TestCase):

    def test_from_list(self):
        persons = []
        for i in range(0, 2):
            persons.append(Person(name='felipe', age=i))

        persons_json = json_util.from_list(persons)
        self.assertEqual([{'name': 'felipe', 'age': 0, 'id': None},
                          {'name': 'felipe', 'age': 1, 'id': None}],
                         persons_json)
