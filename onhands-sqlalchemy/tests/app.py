
from onhands.wsgi.wsgi import application
from onhands.endpoint import endpoint
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from onhands_sqlalchemy.all import AlchemyModel
from onhands.api import OnHandsSettings


Base = declarative_base()


OnHandsSettings.ENDPOINT_MODULES = 'tests.test_endpoint'

@endpoint('/user')
class User(AlchemyModel, Base):
    __tablename__ = 'tb_user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
