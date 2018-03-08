import sys
sys.path.insert(0, '~/Documents/google-cloud-sdk/platform/google_appengine')
sys.path.insert(0, '~/Documents/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.append("./models/")
sys.path.append("./control/")
sys.path.append("./tests/data")
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.api import urlfetch
import json
# import urllib
import unittest
import webtest
import webapp2
from UserHandler import UsersHandler

from randomData import ValidData
from const import MAX_STRING_LENGTH, NUM_TESTS, usersPath, usersURL
from Group import randomGroupEnumString


class UserAPITestCase( unittest.TestCase ):
    def setUp(self):
        app = webapp2.WSGIApplication([(usersPath, UsersHandler)])
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_urlfetch_stub()
        ndb.get_context().clear_cache()
        self.v = ValidData()

    def tearDown(self):
        self.testbed.deactivate()

    def testUsersHandlerPost_Return(self):
        for n in xrange(NUM_TESTS):
            # Create
            url = usersURL
            data = {
                "first_name": self.v.validRandomString( MAX_STRING_LENGTH ),
                "family_name": self.v.validRandomString( MAX_STRING_LENGTH ),
                "group": randomGroupEnumString()
            }
            response = self.testapp.post_json(usersPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)

            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)

            self.assertEqual(payload['first_name'], data["first_name"])
            self.assertEqual(payload['family_name'], data["family_name"])
            self.assertEqual(payload['group'], data["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)

        # for n in xrange(NUM_TESTS):
        #     # Create
        #     url = usersURL
        #     data = {
        #         "first_name": self.v.validRandomString( MAX_STRING_LENGTH ),
        #         "family_name": self.v.validRandomString( MAX_STRING_LENGTH ),
        #         "group": randomGroupEnumString()
        #     }
        #     edata = json.dumps(data)
        #     headers = {'Content-Type': 'application/json'}
        #
        #     # Send
        #     res = urlfetch.fetch(
        #         url=url,
        #         payload=edata,
        #         method=urlfetch.POST,
        #         headers=headers
        #     )
        #
        #     # Check Return
        #     payload = json.loads(res.content)
        #     self.assertEqual("error" in payload.keys(), False)
        #
        #     self.assertEqual("id" in payload.keys(), True)
        #     self.assertEqual("url" in payload.keys(), True)
        #     user_id = payload["id"]
        #     self.assertEqual(payload['url'], usersURL + "/" + user_id)
        #
        #     self.assertEqual(payload['first_name'], data["first_name"])
        #     self.assertEqual(payload['family_name'], data["family_name"])
        #     self.assertEqual(payload['group'], data["group"])
        #     self.assertEqual(payload['device_id'], None)
        #     self.assertEqual(payload['start_datetime'], None)

    def testPostUserReturnsError(self):
        for n in xrange(NUM_TESTS):
            url = usersURL
            data = {}
            if (n % 11) == 0:
                data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                # data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                # data["group"] = randomGroupEnumString()
            if (n % 11) == 1:
                # data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                # data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["group"] = randomGroupEnumString()
            if (n % 11) == 2:
                # Create
                # data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                # data["group"] = randomGroupEnumString()
            if (n % 11) == 3:
                # data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["group"] = randomGroupEnumString()
            if (n % 11) == 4:
                data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                # data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["group"] = randomGroupEnumString()
            if (n % 11) == 5:
                # Create
                data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                # data["group"] = randomGroupEnumString()
            if (n % 11) == 6:
                # Create
                data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["group"] = "Wrong_Group"
            if (n % 11) == 7:
                # Create
                data["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["family_name"] = None
                data["group"] = randomGroupEnumString()
            if (n % 11) == 8:
                # Create
                data["first_name"] = None
                data["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
                data["group"] = randomGroupEnumString()
            if (n % 11) == 9:
                # Create
                data["extra"] = "Extra"
            if (n % 11) == 10:
                data = {}

            # Check Return
            response = self.testapp.post_json(usersPath, data, expect_errors=True)

            # Check Return
            status_int = response.status_int
            self.assertEqual(status_int, 400)

            payload = response.json

            # payload = json.loads(res.content)
            self.assertEqual("error" in payload.keys(), True)
            self.assertEqual("id" in payload.keys(), False)
            self.assertEqual("url" in payload.keys(), False)
            self.assertEqual("first_name" in payload.keys(), False)
            self.assertEqual("family_name" in payload.keys(), False)
            self.assertEqual("group" in payload.keys(), False)


    # def testPostUserInDatastore(self):
    #     for n in xrange(NUM_TESTS):
    #         url = usersURL
    #         data = {}
    #
    #         # Send
    #         res = urlfetch.fetch(
    #             url=url,
    #             method=urlfetch.GET
    #         )
    #         # Check Return
    #         payload = json.loads(res.content)
    #         # self.assertEqual("error" in payload.keys(), True)
    #         self.assertEqual(type(payload) == list, True)
    #         self.assertEqual(len(payload), 0)
    #         # self.assertEqual("url" in payload.keys(), False)
    #         # self.assertEqual("first_name" in payload.keys(), False)
    #         # self.assertEqual("family_name" in payload.keys(), False)
    #         # self.assertEqual("group" in payload.keys(), False)
    #
    # def testGetUserInDatastore(self):
    #     pass
    #
    # def testGetUserNotInDatastore(self):
    #     pass
    #
    # def testGetAllUsersInDatastore(self):
    #     pass
    #
    # def testEditUsersInDatastore(self):
    #     pass
    #
    # def testEditUsersInDatastoreError(self):
    #     pass
    #
    # def testDeleteUsersInDatastore(self):
    #     pass
