from alabama import storage

database = {}


def put(model):
    if model.__name__ in database:
        database[model.__name__].append(model)

storage.put = put


def find(model):
    if model.__name__ in database:
        return database[model.__name__]
    else:
        return []

storage.find = find
