from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import sessionmaker
from onhands.model import Model


class AlchemyModel(Model):
    __engine__ = None

    def __init__(self, *args, **kwargs):
        super(AlchemyModel, self).__init__(self, *args, **kwargs)
        self._session = sessionmaker(bind=self.__engine__)()

    def describe(self):
        pass

    @classmethod
    def columns(cls):
        return sorted([column.key for column in class_mapper(cls).columns])

    def put(self):
        self._session.add(self)
        self._session.commit()
        return self

    def find(self, *args, **kwargs):
        return self._session.query(self.__class__).all()

    def delete(self, *args, **kwargs):
        self._session.query(self.__class__).filter(self.__class__.id == self.id).delete()
        self._session.commit()
        return self

    def get(self, *args, **kwargs):
        return self._session.query(self.__class__).filter(self.__class__.id == self.id).one()
