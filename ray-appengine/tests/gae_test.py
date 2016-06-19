import unittest, os
from google.appengine.api import apiproxy_stub_map, datastore_file_stub
from google.appengine.ext import testbed


class TestCreateEnviroment(unittest.TestCase):

    def setUp(self):
        # fix enviroment
        app_id = 'myapp'
        os.environ['APPLICATION_ID'] = app_id
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        stub = datastore_file_stub.DatastoreFileStub(app_id, '/dev/null', '/')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

        # activate mock services
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
