
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ray_sqlalchemy.all import AlchemyModel
from ray.api import RaySettings


Base = declarative_base()
engine = create_engine('sqlite:///example.db')


RaySettings.ENDPOINT_MODULES.append('app')

@endpoint('/user')
class User(AlchemyModel, Base):
    __tablename__ = 'tb_user'
    __engine__ = engine

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


Base.metadata.create_all(engine)
