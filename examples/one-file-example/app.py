
import peewee
from ray.shield import Shield
from ray.hooks import Hook
from ray.actions import ActionAPI, action
from ray.authentication import Authentication, register
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray_peewee.all import PeeweeModel

from datetime import datetime


database = peewee.SqliteDatabase('example.db')


class PostHook(Hook):

    def before_save(self, post):
        if not post.title:
            raise Exception('Title cannot be None')

        return True

    def before_delete(self, post):
        if post.title:
            raise Exception('You cannot delete a post that has title')

        return True


class DBModel(PeeweeModel):
    class Meta:
        database = database


@register
class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        if username == 'ray' and password == 'charles':
            return {'username': 'ray'}


@endpoint('/post')
class Post(DBModel):
    hooks = [PostHook]

    title = peewee.CharField()
    description = peewee.CharField()


database.create_tables([Post], safe=True)


class PostShield(Shield):
    __model__ = Post

    def put(self, info):
        return info['username'] == 'ray'


class ActionPost(ActionAPI):
    __model__ = Post

    @action("/<id>/upper")
    def upper_case(self, model_id, request_parameters):
        post = Post.get(id=model_id)
        post.update({'title': post.title.upper(), 'id': model_id})

    @action("/now")
    def now_action(self, model_id, request_parameters):
        return datetime.now().strftime('%d/%m/%y')
