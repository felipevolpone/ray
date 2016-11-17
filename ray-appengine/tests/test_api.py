
from google.appengine.ext import ndb
from ray_appengine.all import GAEModel
from .gae_test import TestCreateEnviroment
from ray.endpoint import endpoint


@endpoint('/post')
class User(GAEModel):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()


@endpoint('/post')
class Post(GAEModel):
    title = ndb.StringProperty(required=False)
    text = ndb.StringProperty(required=True)
    owner = ndb.KeyProperty(kind=User)


@endpoint('/notebook')
class Notebook(GAEModel):
    title = ndb.StringProperty(required=True)
    owner = ndb.KeyProperty(kind=User, required=True)


@endpoint('/note')
class Note(GAEModel):
    content = ndb.StringProperty(required=True)

    @classmethod
    def ancestor(cls):
        return (Notebook, 'notebook_id')


class TestInnerMethods(TestCreateEnviroment):

    def test_get_keys(self):
        self.assertEqual(Post._get_keys_and_kinds(), {'owner': 'User'})


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

    def test_update(self):
        self.assertEqual(0, len(User.query().fetch()))
        user = User(name='john', age=25).put()

        to_update = {'name': 'felipe', 'id': user.key.id()}
        User.update(to_update)

        self.assertEqual(1, len(User.query().fetch()))
        user = User.query().fetch()[0]
        self.assertEqual('felipe', user.name)
        self.assertEqual(25, user.age)

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
        new_user.delete()
        all_users = User.query().fetch()
        self.assertEqual(0, len(all_users))

    def test_find_using_keys(self):
        for name, age in [('john', 30), ('maria', 40), ('some', 50), ('felipe', 40)]:
            u = User(name=name, age=age).put()
            Post(owner=u.key, text='any_' + name).put()

        result = Post.find(owner=1)
        result = [p.to_json() for p in result]
        self.assertEqual(result, [{'title': None, 'text': 'any_john', 'id': 2, 'owner': 1}])

        result = Post.find(owner=1, text='any_john')
        result = [p.to_json() for p in result]
        self.assertEqual(result, [{'title': None, 'text': 'any_john', 'id': 2, 'owner': 1}])

        result = Post.find(owner=1, text='any_felipe')
        self.assertEqual(0, len([p.to_json() for p in result]))

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

    def test_store_ancestor(self):
        user = User(name='ray', age=50).put()
        notebook = Notebook(title='notebook', owner=user.key).put()

        note = Note.to_instance({'notebook_id': notebook.key.id(), 'content': 'something'})
        note.put()

        result = Note.find(notebook_id=notebook.key.id())
        self.assertEqual(1, len(result))

        result = Note.find(notebook_id=12123)
        self.assertEqual(0, len(result))

