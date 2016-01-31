from onhands.wsgi.wsgi import application
from onhands.api import OnHandsSettings
from populate import pop
from alabama import connection, storage

database = connection.start_db('db.properties')
connection.create_pool(database)

OnHandsSettings.ENDPOINT_MODULES = 'endpoints'
