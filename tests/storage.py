from alabama import storage

database = {}


def clear():
    global database
    database = {}


def put(model):
    global database
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
