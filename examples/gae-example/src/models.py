
from ray.hooks import Hook
from ray.endpoint import endpoint

from ray_appengine.all import GAEModel
from google.appengine.ext import ndb


class PostHook(Hook):

    def before_save(self, post):
        if len(post.text) < 10:
            raise Exception('The post text cannot so short')
        return True


@endpoint('/post')
class Post(GAEModel):
    hooks = [PostHook]

    title = ndb.StringProperty(required=True)
    text = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=False)


@endpoint('/comment')
class Comments(GAEModel):
    title = ndb.StringProperty(required=False)
    text = ndb.StringProperty(required=True)
    post_key = ndb.KeyProperty(kind=Post)
