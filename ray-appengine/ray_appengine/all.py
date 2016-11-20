
from ray.model import Model
from google.appengine.ext.ndb import Model as AppEngineModel
from google.appengine.ext import ndb
from datetime import datetime


class GAEModel(AppEngineModel, Model):

    @classmethod
    def columns(cls):
        return sorted(cls._properties.keys())

    @classmethod
    def to_instance(cls, json_attributes):
        keys_and_properties = cls._get_keys_and_properties()

        ancestor_kind, ancestor_key = cls.ancestor()
        if not ancestor_kind:
            instance = cls()
        else:
            if ancestor_key not in json_attributes:
                raise Exception('the ancestor key was not found')

            instance = cls(parent=ndb.Key(ancestor_kind, json_attributes[ancestor_key]))
            del json_attributes[ancestor_key]

        for field_name in json_attributes.keys():
            value = json_attributes[field_name]
            if field_name in keys_and_properties:
                json_value = json_attributes[field_name]
                kind, repeated = keys_and_properties[field_name]
                if repeated:
                    value = [ndb.Key(kind, val) for val in json_value]
                else:
                    value = ndb.Key(kind, json_value)

            setattr(instance, field_name, value)
        return instance

    def put(self):
        can_save = Model.put(self)
        if can_save:
            AppEngineModel.put(self)
            return self

    def delete(self, id=None):
        can_delete = Model.delete(self)
        if not id:
            my_key = self
        else:
            my_key = self.__class__.get_by_id(int(id))

        if can_delete and my_key:
            my_key.key.delete()
            return self

    def to_json(self):
        return self.__model_to_json()

    @classmethod
    def ancestor(cls):
        """
            map the usage of the ancestor field in GAEModel

            override this method returning a tuple containing
            (ancestor_kind, json_id)
        """
        return (None, None)

    @classmethod
    def find(cls, *args, **kwargs):
        if not kwargs:
            return cls.query().fetch()

        ancestor_kind, ancestor_key = cls.ancestor()
        if not ancestor_kind and ancestor_key not in kwargs:
            query = cls.query()
        else:
            query = cls.query(ancestor=ndb.Key(ancestor_kind, kwargs[ancestor_key]))
            del kwargs[ancestor_key]

        keys_and_properties = cls._get_keys_and_properties()
        fields_to_filter = set(kwargs.keys())
        keys = set(keys_and_properties.keys())
        fields_arent_keys = fields_to_filter - keys

        for field in fields_arent_keys:
            prop = getattr(cls, field)
            value = kwargs[field]
            if type(value) is list and prop._repeated:
                query = query.filter(prop.IN(value))
            else:
                query = query.filter(prop == value)

        if bool(fields_to_filter & keys):  # check if there are keys in the fields to filter
            for key, prop in keys_and_properties.items():
                key_id = kwargs[key]
                kind, repeated = prop
                if type(key_id) is list and repeated:
                    query = query.filter(getattr(cls, key).IN(key_id))
                else:
                    query = query.filter(getattr(cls, key) == ndb.Key(kind, key_id))

        return query.fetch()

    @classmethod
    def get(cls, id=None):
        return cls.get_by_id(int(id))

    @classmethod
    def update(cls, fields_to_update):
        if 'id' not in fields_to_update:
            raise Exception('You should provide an id')

        entity = ndb.Key(cls.__name__, fields_to_update['id']).get()

        for key, value in fields_to_update.items():
            if key in entity._properties:
                value = cls.from_raw_to_type(cls._properties[key], value)
                setattr(entity, key, value)

        entity.put()
        return entity

    @classmethod
    def _get_keys_and_properties(cls):
        keys = {}
        for name, property_type in cls._properties.items():
            if isinstance(property_type, ndb.KeyProperty):
                keys[name] = property_type._kind, property_type._repeated

        return keys

    def __model_to_json(self):
        model_json = {}
        for prop in self._properties:
            value = getattr(self, prop)
            model_json[prop] = self.__class__.__from_type_to_raw_value(self._properties[prop], value)

        if 'id' in dir(self.key):
            model_json['id'] = self.key.id()

        return model_json

    @classmethod
    def from_raw_to_type(cls, field, value):
        return cls.__from_raw_to_type(field, value)

    @classmethod
    def __from_type_to_raw_value(cls, field, value):
        types = {'StringProperty': cls.__decode_str,
                 'IntegerProperty': cls.__to_int,
                 'FloatProperty': cls.__to_float,
                 'DateTimeProperty': cls._convert_date,
                 'BooleanProperty': bool,
                 'BlobKeyProperty': cls.__blob_to_url,
                 'TextProperty': cls.__decode_str,
                 'KeyProperty': cls.__key_property_to_id}

        field_type = type(field).__name__
        return types[field_type](value) if field_type in types else None

    @classmethod
    def __from_raw_to_type(cls, field, value):
        types = {'StringProperty': cls.__decode_str,
                 'IntegerProperty': cls.__to_int,
                 'FloatProperty': cls.__to_float,
                 'DateTimeProperty': cls._str_to_date,
                 'BooleanProperty': bool,
                 'TextProperty': cls.__decode_str}

        field_type = type(field).__name__
        value = cls.__decode_str(value)
        return types[field_type](value) if field_type in types else None

    @classmethod
    def _convert_date(cls, date):
        if type(date) == datetime:
            return date.strftime("%d/%m/%Y")
        else:
            return cls._str_to_date(date)

    @classmethod
    def __key_property_to_id(cls, key):
        if not key:
            return None

        if type(key) is list:
            return [k.id() for k in key]

        return key.id()

    @classmethod
    def __to_int(cls, value):
        if not value:
            return 0
        elif type(value) is list:
            return value
        return int(value)

    @classmethod
    def __to_float(cls, value):
        if not value:
            return 0.0
        elif type(value) is list:
            return value
        return float(value)

    @classmethod
    def __blob_to_url(self, blob):
        return str(blob)

    @classmethod
    def _str_to_date(cls, data):
        if not data:
            return None
        date_parts = data.split('/')
        date = (datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])))
        return date

    @classmethod
    def __decode_str(cls, value):
        if isinstance(value, str):
            return value
        if isinstance(value, unicode):
            return value.encode('utf-8')
        return value
