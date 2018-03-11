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
from webapp2 import Route
from UserHandler import UsersHandler, UserHandler
from webapp2_extras.routes import RedirectRoute, PathPrefixRoute

from randomData import ValidData
from const import MAX_STRING_LENGTH, NUM_TESTS, usersPath, usersURL
from Group import randomGroupEnumString


class UserAPITestCase( unittest.TestCase ):
    def setUp(self):
        allowed_methods = webapp2.WSGIApplication.allowed_methods
        new_allowed_methods = allowed_methods.union(('PATCH',))
        webapp2.WSGIApplication.allowed_methods = new_allowed_methods
        app = webapp2.WSGIApplication([
            Route('/users', handler=UsersHandler, name='users'),
            PathPrefixRoute( '/users',[
                Route('/', handler=UsersHandler, name='users'),
                Route('/<user_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=UserHandler, name='user'),]), ])
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
                data["extra"] = "Extra" + str(n);
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

    def testPostUserIsAddedToDatastore(self):
        # Post User and ensure it is added to Datastore GET ALL
        for n in xrange(NUM_TESTS):
            url = usersURL
            # PRE: GET ALL Users
            response = self.testapp.get(usersURL);
            pre_payload = response.json
            self.assertEqual(type(pre_payload), list);
            for i in pre_payload:
                obj = json.loads(i)
                self.assertEqual(type(obj), dict)
                self.assertEqual('error' in obj.keys(), False)
                self.assertEqual("id" in payload.keys(), True)
                self.assertEqual("url" in payload.keys(), True)
                user_id = payload["id"]
                self.assertEqual(payload['url'], usersURL + "/" + user_id)
                self.assertEqual('first_name' in obj.keys(), True)
                self.assertEqual('family_name' in obj.keys(), True)
                self.assertEqual('group' in obj.keys(), True)
                self.assertEqual('device_id' in obj.keys(), True)
                self.assertEqual('start_datetime' in obj.keys(), True)

            # Add New
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
            self.assertEqual("first_name" in payload.keys(), True)
            self.assertEqual("family_name" in payload.keys(), True)
            self.assertEqual("group" in payload.keys(), True)
            self.assertEqual("device_id" in payload.keys(), True)
            self.assertEqual("start_datetime" in payload.keys(), True)
            self.assertEqual(payload['first_name'], data["first_name"])
            self.assertEqual(payload['family_name'], data["family_name"])
            self.assertEqual(payload['group'], data["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)

            # Check Object added to GET ALL
            # AFTER: GET ALL Users
            response = self.testapp.get(usersURL);
            post_payload = response.json
            self.assertEqual(type(post_payload), list);
            for i in xrange(len(post_payload)):
                obj = json.loads(post_payload[i])
                self.assertEqual(type(obj), dict)
                self.assertEqual('error' in obj.keys(), False)
                self.assertEqual("id" in payload.keys(), True)
                self.assertEqual("url" in payload.keys(), True)
                user_id = payload["id"]
                self.assertEqual(payload['url'], usersURL + "/" + user_id)
                self.assertEqual('first_name' in obj.keys(), True)
                self.assertEqual('family_name' in obj.keys(), True)
                self.assertEqual('group' in obj.keys(), True)
                self.assertEqual('device_id' in obj.keys(), True)
                self.assertEqual('start_datetime' in obj.keys(), True)
                if i < len(pre_payload):
                    pre_obj = json.loads(pre_payload[i])
                    self.assertEqual(pre_obj['first_name'], obj['first_name'])
                    self.assertEqual(pre_obj['family_name'], obj['family_name'])
                    self.assertEqual(pre_obj['group'], obj['group'])
                    self.assertEqual(pre_obj['device_id'], obj['device_id'])
                    self.assertEqual(pre_obj['start_datetime'], obj['start_datetime'])
                else:
                    # compare posted object to this one
                    self.assertEqual(data['first_name'], obj['first_name'])
                    self.assertEqual(data['family_name'], obj['family_name'])
                    self.assertEqual(data['group'], obj['group'])
                    self.assertEqual(None, obj['device_id'])
                    self.assertEqual(None, obj['start_datetime'])

    def testGetUserInDatastore(self):
        # Post User and ensure it is added to Datastore GET ONE
        for n in xrange(NUM_TESTS):
            url = usersURL
            # Add New
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
            self.assertEqual("first_name" in payload.keys(), True)
            self.assertEqual("family_name" in payload.keys(), True)
            self.assertEqual("group" in payload.keys(), True)
            self.assertEqual("device_id" in payload.keys(), True)
            self.assertEqual("start_datetime" in payload.keys(), True)
            self.assertEqual(payload['first_name'], data["first_name"])
            self.assertEqual(payload['family_name'], data["family_name"])
            self.assertEqual(payload['group'], data["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Users via payload['url']
            response = self.testapp.get(payload['url']);
            post_payload = response.json
            obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)
            self.assertEqual('first_name' in obj.keys(), True)
            self.assertEqual('family_name' in obj.keys(), True)
            self.assertEqual('group' in obj.keys(), True)
            self.assertEqual('device_id' in obj.keys(), True)
            self.assertEqual('start_datetime' in obj.keys(), True)
            self.assertEqual(data['first_name'], obj['first_name'])
            self.assertEqual(data['family_name'], obj['family_name'])
            self.assertEqual(data['group'], obj['group'])
            self.assertEqual(None, obj['device_id'])
            self.assertEqual(None, obj['start_datetime'])

    def testEditUsersInDatastore(self):
        for n in xrange(NUM_TESTS):
            url = usersURL
            # Add New
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
            self.assertEqual("first_name" in payload.keys(), True)
            self.assertEqual("family_name" in payload.keys(), True)
            self.assertEqual("group" in payload.keys(), True)
            self.assertEqual("device_id" in payload.keys(), True)
            self.assertEqual("start_datetime" in payload.keys(), True)
            self.assertEqual(payload['first_name'], data["first_name"])
            self.assertEqual(payload['family_name'], data["family_name"])
            self.assertEqual(payload['group'], data["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Users via payload['url']
            response = self.testapp.get(payload['url']);
            post_payload = response.json
            obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual('first_name' in obj.keys(), True)
            self.assertEqual('family_name' in obj.keys(), True)
            self.assertEqual('group' in obj.keys(), True)
            self.assertEqual('device_id' in obj.keys(), True)
            self.assertEqual('start_datetime' in obj.keys(), True)
            self.assertEqual(data['first_name'], obj['first_name'])
            self.assertEqual(data['family_name'], obj['family_name'])
            self.assertEqual(data['group'], obj['group'])
            self.assertEqual(None, obj['device_id'])
            self.assertEqual(None, obj['start_datetime'])

            # Edit Object
            obj_new = {}
            obj_new["first_name"] = obj["first_name"]
            obj_new["family_name"] = obj["family_name"]
            obj_new["group"] = obj["group"]

            if (n % 3 == 0):
                obj_new["first_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
            elif (n % 3 == 1):
                obj_new["family_name"] = self.v.validRandomString( MAX_STRING_LENGTH )
            elif (n % 3 == 2):
                obj_new["group"] = randomGroupEnumString()

            response = self.testapp.patch_json(payload['url'], obj_new)

            # Check Object changed
            response = self.testapp.get(payload['url']);
            post_payload = response.json
            obj2 = json.loads(post_payload)
            self.assertEqual('error' in obj2.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)
            self.assertEqual('first_name' in obj2.keys(), True)
            self.assertEqual('family_name' in obj2.keys(), True)
            self.assertEqual('group' in obj2.keys(), True)
            self.assertEqual('device_id' in obj2.keys(), True)
            self.assertEqual('start_datetime' in obj2.keys(), True)
            self.assertEqual(obj_new['first_name'], obj2['first_name'])
            self.assertEqual(obj_new['family_name'], obj2['family_name'])
            self.assertEqual(obj_new['group'], obj2['group'])
            self.assertEqual(None, obj2['device_id'])
            self.assertEqual(None, obj2['start_datetime'])

            if (n % 3 == 0):
                self.assertNotEqual(data['first_name'], json.dumps(obj2['first_name']))
            elif (n % 3 == 1):
                self.assertNotEqual(data['family_name'], json.dumps(obj2['family_name']))
            elif (n % 3 == 2):
                self.assertNotEqual(data['group'], json.dumps(obj2['group']))

            return

    def testEditUsersInDatastoreError(self):
        # Too much info
        # No Changes
        for n in xrange(NUM_TESTS):
            url = usersURL
            # Add New
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
            self.assertEqual("first_name" in payload.keys(), True)
            self.assertEqual("family_name" in payload.keys(), True)
            self.assertEqual("group" in payload.keys(), True)
            self.assertEqual("device_id" in payload.keys(), True)
            self.assertEqual("start_datetime" in payload.keys(), True)
            self.assertEqual(payload['first_name'], data["first_name"])
            self.assertEqual(payload['family_name'], data["family_name"])
            self.assertEqual(payload['group'], data["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Users via payload['url']
            response = self.testapp.get(payload['url']);
            post_payload = response.json
            obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)
            self.assertEqual('first_name' in obj.keys(), True)
            self.assertEqual('family_name' in obj.keys(), True)
            self.assertEqual('group' in obj.keys(), True)
            self.assertEqual('device_id' in obj.keys(), True)
            self.assertEqual('start_datetime' in obj.keys(), True)
            self.assertEqual(data['first_name'], obj['first_name'])
            self.assertEqual(data['family_name'], obj['family_name'])
            self.assertEqual(data['group'], obj['group'])
            self.assertEqual(None, obj['device_id'])
            self.assertEqual(None, obj['start_datetime'])

            # Edit Object Invalid
            obj_new = {}
            obj_new["first_name"] = obj["first_name"]
            obj_new["family_name"] = obj["family_name"]
            obj_new["group"] = obj["group"]

            if (n % 3 == 0):
                obj_new = {}
            elif (n % 3 == 1):
                obj_new["extra"] = "extra"
            # elif (n % 3 == 2): Keep same

            response = self.testapp.patch_json(payload['url'], obj_new, expect_errors=True)
            obj2 = response.json
            self.assertEqual('error' in obj2.keys(), True)

            # Check Object did NOT changed
            response = self.testapp.get(payload['url']);
            post_payload = response.json
            obj2 = json.loads(post_payload)
            self.assertEqual('error' in obj2.keys(), False  )
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)
            self.assertEqual('first_name' in obj2.keys(), True)
            self.assertEqual('family_name' in obj2.keys(), True)
            self.assertEqual('group' in obj2.keys(), True)
            self.assertEqual('device_id' in obj2.keys(), True)
            self.assertEqual('start_datetime' in obj2.keys(), True)

            self.assertEqual(data['first_name'], obj2['first_name'])
            self.assertEqual(data['family_name'], obj2['family_name'])
            self.assertEqual(data['group'], obj2['group'])
            self.assertEqual(None, obj2['device_id'])
            self.assertEqual(None, obj2['start_datetime'])

            return

    def testDeleteUsersInDatastore(self):
        # Create, Verify, Delete Verify
        for n in xrange(NUM_TESTS):
            url = usersURL
            # Add New
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
            self.assertEqual("first_name" in payload.keys(), True)
            self.assertEqual("family_name" in payload.keys(), True)
            self.assertEqual("group" in payload.keys(), True)
            self.assertEqual("device_id" in payload.keys(), True)
            self.assertEqual("start_datetime" in payload.keys(), True)
            self.assertEqual(payload['first_name'], data["first_name"])
            self.assertEqual(payload['family_name'], data["family_name"])
            self.assertEqual(payload['group'], data["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Users via payload['url']
            response = self.testapp.get(payload['url']);
            post_payload = response.json
            obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)
            self.assertEqual('first_name' in obj.keys(), True)
            self.assertEqual('family_name' in obj.keys(), True)
            self.assertEqual('group' in obj.keys(), True)
            self.assertEqual('device_id' in obj.keys(), True)
            self.assertEqual('start_datetime' in obj.keys(), True)
            self.assertEqual(data['first_name'], obj['first_name'])
            self.assertEqual(data['family_name'], obj['family_name'])
            self.assertEqual(data['group'], obj['group'])
            self.assertEqual(None, obj['device_id'])
            self.assertEqual(None, obj['start_datetime'])

            # Delete Object
            response = self.testapp.delete(payload['url'])
            self.assertEqual(response.status_int, 204)

            # Check Object Not there
            response = self.testapp.get(payload['url'], expect_errors=True);
            self.assertEqual(response.status_int, 404)
