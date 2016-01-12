from alabama import storage
import uuid

database = {}


def __uuid():
    return str(uuid.uuid4())


def clear():
    global database
    database = {}


def put(model):
    global database
    model.uuid = __uuid()
    if model.__class__.__name__ in database:
        database[model.__class__.__name__].append(model)
    else:
        database[model.__class__.__name__] = [model]
    return model

storage.put = put


def find(model):
    global database
    if model.__class__.__name__ in database:
        return database[model.__class__.__name__]
    else:
        return []

storage.find = find


def get(cls, uuid):
    global database
    if cls.__class__.__name__ in database:
        for model in database[cls.__class__.__name__]:
            if model.uuid == uuid:
                return model
