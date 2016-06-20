
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import sessionmaker
from ray.model import Model


class AlchemyModel(Model):
    __engine__ = None

    def __init__(self, *args, **kwargs):
        super(AlchemyModel, self).__init__(self, *args, **kwargs)
        self._session = sessionmaker(bind=self.__engine__)()

    @classmethod
    def columns(cls):
        return sorted([column.key for column in class_mapper(cls).columns])

    def put(self):
        super(AlchemyModel, self).put()

        if self.id:
            self._session.query(self.__class__).filter(self.__class__.id == self.id).update(self.to_json())
        else:
            self._session.add(self)

        self._session.commit()
        return self

    @classmethod
    def find(cls, *args, **kwargs):
        if not kwargs:
            return self._session.query(cls).all()

        query = self._session.query(cls)
        for field, value in kwargs.items():
            query = query.filter(getattr(cls, field) == value)

        return query.all()

    def delete(self, *args, **kwargs):
        super(AlchemyModel, self).delete()

        self._session.query(self.__class__).filter(self.__class__.id == self.id).delete()
        self._session.commit()
        return self

    @classmethod
    def get(cls, id=None):
        return self._session.query(cls).filter(cls.id == id).one()
