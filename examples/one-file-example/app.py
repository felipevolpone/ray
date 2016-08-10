
import peewee
from ray.shield import Shield
from ray.hooks import Hook
from ray.actions import ActionAPI, action
from ray.authentication import Authentication
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray_peewee.all import PeeweeModel


database = peewee.SqliteDatabase('example.db')


class PostHook(Hook):

    def before_save(self, post):
        if not post.title:
            raise Exception('Title cannot be None')

        return True

    def before_delete(self, post):
        if post.title:
            print 'veio lancar a excecao'
            raise Exception('You cannot delete a post that has title')

        return True


class DBModel(PeeweeModel):
    class Meta:
        database = database


@endpoint('/post')
class Post(DBModel):
    hooks = [PostHook]

    title = peewee.CharField()
    description = peewee.CharField()


database.create_tables([Post], safe=True)


# class PostShield(Shield):
#     __model__ = Post

#     def put(self, info):
#         return info['username'] == 'felipe'


# class MyAuth(Authentication):

#     @classmethod
#     def authenticate(cls, username, password):
#         if username == 'felipe' and password == '123':
#             return {'username': 'felipe'}


class ActionPost(ActionAPI):
    __model__ = Post

    @action("/upper")
    def upper_case(self, model_id):
        pass
        # post = s.query(Post).filter(Post.id == model_id).all()[0]
        # post.title = post.title.upper()
        # s.add(post)
        # s.commit()
