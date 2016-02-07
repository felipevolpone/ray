from onhands.wsgi.wsgi import application
from onhands.api import OnHandsSettings
from alabama import connection

database = connection.start_db('db.properties')
connection.create_pool(database)

OnHandsSettings.ENDPOINT_MODULES = 'endpoints'
