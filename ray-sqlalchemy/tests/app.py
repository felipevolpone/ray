
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint, RaySettings
from ray_sqlalchemy.all import AlchemyModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


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
