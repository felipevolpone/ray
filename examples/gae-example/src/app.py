from ray import login
from ray.authentication import Authentication, register
from ray.endpoint import endpoint
from ray.hooks import DatabaseHook
from ray.wsgi.wsgi import application

from ray_appengine.all import GAEModel
from google.appengine.ext import ndb


# Google App Engine will start the app automatically,
# since the embedded WSGI server is looking for an
# attribute called 'app'.
app = application


class UserHook(DatabaseHook):

    def before_save(self, user):
        users_same_username = User.query(User.username == user.username).fetch(1)
        if any(users_same_username):
            raise Exception('The username is unique')

        return True


@endpoint('/user')
class User(GAEModel):
    hooks = [UserHook]

    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)


@register
class SimpleNoteAuthentication(Authentication):

    salt_key = 'anything'

    @classmethod
    def authenticate(cls, login_data):
        users = User.query(User.username == login_data['username'],
                           User.password == login_data['password']).fetch(1)
        if not any(users):
            raise Exception('Wrong username or/and password')

        return users[0].to_json()


class NoteHook(DatabaseHook):

    def before_save(self, note):
        if not note.title:
            raise Exception('Title cannot be None')

        if not note.notebook:
            raise Exception('A note only exists inside a notebook')

        if not note.notebook.get():
            raise Exception('Invalid notebook')

        return True


class NotebookHook(DatabaseHook):

    def before_save(self, notebook):
        if not notebook.title:
            raise Exception('Title cannot be None')

        logged_user = SimpleNoteAuthentication.get_logged_user()
        notebook.owner = ndb.Key(User, logged_user['id'])
        return True


@endpoint('/notebook', authentication=SimpleNoteAuthentication)
class Notebook(GAEModel):
    hooks = [NotebookHook]

    title = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.KeyProperty(required=True, kind=User)


@endpoint('/note', authentication=SimpleNoteAuthentication)
class Note(GAEModel):
    hooks = [NoteHook]

    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    notebook = ndb.KeyProperty(required=True, kind=Notebook)
    created_at = ndb.DateTimeProperty(auto_now_add=True)


