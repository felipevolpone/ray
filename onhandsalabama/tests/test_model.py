import unittest
from onhandsalabama.all import AlabamaModel
from alabama import connection


class TestLoader(unittest.TestCase):
    def setUp(self):
        database = connection.start_db('tests/db.properties')
        connection.create_pool(database)


class TestAlabamaModel(unittest.TestCase):
    def test(self):
        model = AlabamaModel()
        self.assertTrue(hasattr(model, 'put'))
        self.assertTrue(hasattr(model, 'delete'))


class TestIntegration(TestLoader):
    def test_api(self):
        pass
