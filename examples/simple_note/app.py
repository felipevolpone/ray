
from playhouse.shortcuts import dict_to_model, model_to_dict  # peewee
import peewee

from datetime import datetime

from ray.authentication import Authentication, register
from ray.hooks import DatabaseHook
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray_peewee.all import PeeweeModel
from ray.actions import Action, action
from ray.shield import Shield


database = peewee.SqliteDatabase('example.db')


class DBModel(PeeweeModel):
    class Meta:
        database = database


class MailHelper(object):

    @classmethod
    def send_email(self, to, message):
        # fake send email
        print('sending email to: %s with message: %s' % (to, message))


class UserHook(DatabaseHook):

    def before_save(self, user):
        users_same_username = (User.select()
                                   .where(User.username == user.username))
        if any(users_same_username):
            raise Exception('The username is unique')

        return True


class User(DBModel):
    hooks = [UserHook]

    username = peewee.CharField()
    password = peewee.CharField()
    profile = peewee.CharField()


@register
class SimpleNoteAuthentication(Authentication):

    salt_key = 'anything'
    expiration_time = 5

    @classmethod
    def authenticate(cls, login_data):
        users = User.select().where(User.username == login_data['username'],
                                    User.password == login_data['password'])
        if not any(users):
            raise Exception('Wrong username or/and password')

        return users[0].to_json()


class CreatedAtBaseHook(DatabaseHook):

    def before_save(self, model):
        model.update_at = int(datetime.now().strftime('%s')) * 1000
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
    update_at = peewee.BigIntegerField()
    owner = peewee.ForeignKeyField(User)
    active = peewee.BooleanField(default=True)


@endpoint('/note', authentication=SimpleNoteAuthentication)
class Note(DBModel):
    hooks = [NoteHook]

    title = peewee.CharField()
    update_at = peewee.BigIntegerField()
    content = peewee.TextField()
    notebook = peewee.ForeignKeyField(Notebook)


class NotebookShield(Shield):
    __model__ = Notebook

    def delete(self, user_data, notebook_id, parameters):
        return user_data['profile'] == Profile.ADMIN

    @staticmethod
    def only_owner_can_deactivate(user_data, notebook_id, parameters):
        notebook = Notebook.select().where(Notebook.id == int(notebook_id))[0]
        notebook_json = model_to_dict(notebook, recurse=False)
        return user_data['id'] == notebook_json['owner']


class NotebookActions(Action):
    __model__ = Notebook

    @action('/<id>/invite', authentication=True)
    def invite_to_notebook(self, notebook_id, parameters):
        to = parameters['user_to_invite']
        title = Notebook.select().where(Notebook.id == notebook_id)[0].title
        message = 'Help me build new stuff in this notebook: %s' % (title)
        MailHelper.send_email(to, message)

    @action('/<id>/deactivate', protection=NotebookShield.only_owner_can_deactivate, authentication=True)
    def deactivate(self, notebook_id, parameters):
        notebook = Notebook.select().where(Notebook.id == int(notebook_id))[0]
        notebook.active = False
        notebook.update()


class Profile(object):
    ADMIN = 'admin'
    DEFAULT = 'default'


if __name__ == '__main__':
    database.connect()
    database.create_tables([User, Notebook, Note], safe=True)
    User.create(username='admin', password='admin', profile=Profile.ADMIN)
    User.create(username='john', password='123', profile=Profile.DEFAULT)
    database.close()
    application.run(debug=True, reloader=True)
