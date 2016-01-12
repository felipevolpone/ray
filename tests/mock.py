from onhands.http import Response
import unittest
from tests import storage


class MockResponse(Response):

    def __init__(self, instance):
        Response.__init__(self, instance.json)

    def to_json(self):
        result = {}
        if not self._json:
            return {}

        for key, value in self._json.items():
            key = key.encode('utf-8')
            if type(value) is unicode:
                value = value.encode('utf-8')

            result[key] = value
        return result


class TestMock(unittest.TestCase):

    def setUp(self):
        storage.clear()
