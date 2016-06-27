
from ray.hooks import Hook
from ray.endpoint import endpoint, RaySettings
from ray.wsgi.wsgi import application

from ray_appengine.all import GAEModel
from google.appengine.ext import ndb
from google.appengine.ext.ndb import Model


RaySettings.ENDPOINT_MODULES.append('src.models')


class PostHook(Hook):

    def before_save(self, post):
        if len(post.text) < 140:
            raise Exception('The post text cannot be a tweet')
        return True


@endpoint('/post')
class Post(GAEModel):
    hooks = [PostHook]

    title = ndb.StringProperty(required=True)
    text = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=False)
    # created_at = ndb.IntegerProperty(required=True)
