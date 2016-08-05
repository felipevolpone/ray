
import unittest, peewee
from ray_peewee.all import PeeweeModel


database = peewee.SqliteDatabase('example.db')


class DBModel(PeeweeModel):
    class Meta:
        database = database


class User(DBModel):
    name = peewee.CharField()
    age = peewee.IntegerField()


class TestRayPeeweeAPI(unittest.TestCase):

    def test_columns(self):
        self.assertEqual(['age', 'id', 'name'], User.columns())

    def test_to_instance(self):
        new_user = User.to_instance({'age': 99, 'name': 'Frank Sinatra'})
        self.assertEqual(99, new_user.age)
        self.assertEqual('Frank Sinatra', new_user.name)
