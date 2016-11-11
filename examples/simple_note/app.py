
from playhouse.shortcuts import model_to_dict, dict_to_model  # peewee
import peewee

from datetime import datetime

from ray.authentication import Authentication, register
from ray import login
from ray.hooks import DatabaseHook
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray_peewee.all import PeeweeModel


database = peewee.SqliteDatabase('example.db')


class DBModel(PeeweeModel):
    class Meta:
        database = database


class UserHook(DatabaseHook):

    def before_save(self, user):
        users_same_username = User.select().where(User.username == user.username)
        if any(users_same_username):
            raise Exception('The username is unique')

        return True


class User(DBModel):
    hooks = [UserHook]

    username = peewee.CharField()
    password = peewee.CharField()


@register
class SimpleNoteAuthentication(Authentication):

    salt_key = 'anything'

    @classmethod
    def authenticate(cls, login_data):
        users = User.select().where(User.username == login_data['username'], User.password == login_data['password'])
        if not any(users):
            raise Exception('Wrong username or/and password')

        return users[0].to_json()


class CreatedAtBaseHook(DatabaseHook):

    def before_save(self, model):
        model.created_at = int(datetime.now().strftime('%s')) * 1000
        return True


class NoteHook(CreatedAtBaseHook):

    def before_save(self, note):
        super(NoteHook, self).before_save(note)

        if not note.title:
            raise Exception('Title cannot be None')

        if not note.notebook_id:
            raise Exception('A note only exists inside a notebook')

        return True


class NotebookHook(CreatedAtBaseHook):

    def before_save(self, notebook):
        super(NotebookHook, self).before_save(notebook)

        if not notebook.title:
            raise Exception('Title cannot be None')

        notebook.owner = dict_to_model(User, SimpleNoteAuthentication.get_logged_user())
        return True


@endpoint('/notebook', authentication=SimpleNoteAuthentication)
class Notebook(DBModel):
    hooks = [NotebookHook]

    title = peewee.CharField()
    created_at = peewee.BigIntegerField()
    owner = peewee.ForeignKeyField(User)


@endpoint('/note', authentication=SimpleNoteAuthentication)
class Note(DBModel):
    hooks = [NoteHook]

    title = peewee.CharField()
    created_at = peewee.BigIntegerField()
    content = peewee.TextField()
    notebook = peewee.ForeignKeyField(Notebook)


if __name__ == '__main__':
    database.create_tables([User, Notebook, Note], safe=True)
    User.create(username='admin', password='admin')
    application.run(debug=True, reloader=True)
