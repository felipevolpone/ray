
from ray.shield import Shield
from ray.hooks import Hook
from ray.actions import ActionAPI, action
from ray.authentication import Authentication
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray_sqlalchemy.all import AlchemyModel

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///example_blog.db')
Session = sessionmaker(bind=engine)


class PostHook(Hook):

    def before_save(self, post):
        if not post.title:
            raise Exception('Title cannot be None')
        return True


@endpoint('/post')
class Post(AlchemyModel, Base):
    __tablename__ = 'tb_post'
    __engine__ = engine

    hooks = [PostHook]

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Integer)
    author = Column(String)


Base.metadata.create_all(engine)


class PostShield(Shield):
    __model__ = Post

    def put(self, info):
        return info['username'] == 'felipe'


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        if username == 'felipe' and password == '123':
            return {'username': 'felipe'}


class ActionPost(ActionAPI):
    __model__ = Post

    @action("/upper")
    def upper_case(self, model_id):
        s = Session()
        post = s.query(Post).filter(Post.id == model_id).all()[0]
        post.title = post.title.upper()
        s.add(post)
        s.commit()
