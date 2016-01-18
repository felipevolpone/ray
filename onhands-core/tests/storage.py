from alabama import storage
import uuid

database = {}


def __uuid():
    return str(uuid.uuid4())


def clear():
    global database
    database = {}


def delete(model, uuid):
    new_model = model.__class__()
    new_model.uuid = uuid
    return new_model

storage.delete = delete


def __update_model(new_model):
    if new_model.__class__.__name__ in database:
        for model in database[new_model.__class__.__name__]:
            if model.uuid == new_model.uuid:
                for column in new_model.columns():
                    if getattr(new_model, column) is not None:
                        setattr(model, column, getattr(new_model, column))
                return model


def put(model):
    global database
    if model.uuid:
        return __update_model(model)

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
