from alabama import connection, storage
from endpoints import User


def pop():
    database = connection.start_db('db.properties')
    connection.create_pool(database)
    storage.create_database(User)
    connection.my_connection().commit()

if __name__ == '__main__':
    pop()
