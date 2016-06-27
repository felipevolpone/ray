
from google.appengine.ext import ndb
from ray_appengine.all import GAEModel
from .gae_test import TestCreateEnviroment
from ray.endpoint import endpoint, RaySettings


RaySettings.ENDPOINT_MODULES.append('test_api')


@endpoint('/post')
class User(GAEModel):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()


@endpoint('/post')
class Post(GAEModel):
    title = ndb.StringProperty(required=False)
    text = ndb.StringProperty(required=True)
    owner = ndb.KeyProperty(kind=User)


class TestIntegrated(TestCreateEnviroment):

    def test_columns(self):
        columns = User.columns()
        self.assertEqual(['age', 'name'], columns)

    def test_put(self):
        User(name='john', age=25).put()
        all_users = User.query().fetch()
        self.assertEqual(1, len(all_users))

    def test_put_foreign_key(self):
        owner = User(name='john', age=25).put()
        new_post = Post.to_instance({'text': 'any', 'owner': owner.to_json()['id']})
        self.assertTrue(new_post.put())

        posts = Post.query().fetch()
        self.assertEqual(1, len(posts))
        self.assertEqual(owner.to_json()['id'], posts[0].owner.id())

    def test_to_json(self):
        u = User(name='felipe', age=33).put()
        expected = {'name': 'felipe', 'age': 33, 'id': 1}
        self.assertEqual(expected, u.to_json())

    def test_delete(self):
        # setup
        new_user = User(name='john', age=25)
        new_user.put()
        all_users = User.query().fetch()
        self.assertEqual(1, len(all_users))

        # delete
        new_user.remove()
        all_users = User.query().fetch()
        self.assertEqual(0, len(all_users))

    def test_find(self):
        # setup
        for name, age in [('john', 30), ('maria', 40), ('some', 50), ('felipe', 40)]:
            User(name=name, age=age).put()

        # testing one param
        result = User.find(name='maria')
        result = [u.to_json() for u in result]
        self.assertEqual(result, [{'age': 40, 'name': u'maria', 'id': 2}])

        # testing select all
        result = User.find()
        result = [u.to_json() for u in result]
        self.assertEqual(result, [{'age': 30, 'name': u'john', 'id': 1}, {'age': 40, 'name': u'maria', 'id': 2},
                                  {'age': 50, 'name': u'some', 'id': 3}, {'name': 'felipe', 'age': 40, 'id': 4}])

        # testing one param with more than one result
        result = User.find(age=40)
        result = [u.to_json() for u in result]
        self.assertEqual(result, [{'age': 40, 'name': u'maria', 'id': 2}, {'name': 'felipe', 'age': 40, 'id': 4}])

        # testing two param with more than one result
        result = User.find(age=40, name='maria')
        result = [u.to_json() for u in result]
        self.assertEqual(result, [{'age': 40, 'name': u'maria', 'id': 2}])

    def test_get(self):
        ids = []
        for name, age in [('john', 30), ('maria', 40), ('some', 50), ('felipe', 40)]:
            ids.append(User(name=name, age=age).put().key.id())

        user = User.get(ids[0])
        self.assertEqual('john', user.name)

        user = User.get(ids[-1])
        self.assertEqual('felipe', user.name)
