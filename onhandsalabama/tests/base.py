import unittest
from alabama import connection
from onhandsalabama.all import AlabamaModel
from alabama.models import StringProperty, IntegerProperty


class TestLoader(unittest.TestCase):
    def setUp(self):
        database = connection.start_db('tests/db.properties')
        connection.create_pool(database)
