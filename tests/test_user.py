
import sys
sys.path.insert(0, '~/Documents/google-cloud-sdk/platform/google_appengine')
sys.path.insert(0, '~/Documents/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.append("./models/")
sys.path.append("./tests/data")

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest
import json
from randomData import ValidData
from const import MAX_STRING_LENGTH, NUM_TESTS, usersURL
from User import User
from Group import Group, randomGroupEnum, randomGroupEnumString


def GetEntityViaMemcache(entity_key):
    # Get from memcache, then try datastore
    if entity == memcache.get(entity_key):
        return entity

    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


class UserDatastoreTestCase( unittest.TestCase ):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        self.v = ValidData()

    def tearDown(self):
        self.testbed.deactivate()

    def testInsertUser(self):
        for n in xrange(NUM_TESTS):
            user = User()
            user.first_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.family_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.group = randomGroupEnum()
            user.device_id = self.v.validRandomString(MAX_STRING_LENGTH)
            user.start_datetime = self.v.validRandomDateTime()
            user_key = user.put()
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, user.device_id)
            self.assertEqual(q[n].start_datetime, user.start_datetime)

    def testSerializeUserWithDevice(self):
        for n in xrange(NUM_TESTS):
            user = User()
            user.first_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.family_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.group = randomGroupEnum()
            user.device_id = self.v.validRandomString(MAX_STRING_LENGTH)
            user.start_datetime = self.v.validRandomDateTime()
            user_key = user.put()
            q = User.query().fetch(n+1)
            v = q[n].serializeUser(usersURL)
            v_json = json.loads(v)
            self.assertNotEqual(v, None)
            self.assertEqual(v_json["first_name"], q[n].first_name)

    def testSerializeUserWithOutDevice(self):
        for n in xrange(NUM_TESTS):
            user = User()
            user.first_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.family_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.group = randomGroupEnum()
            user_key = user.put()
            q = User.query().fetch(n+1)
            v = q[n].serializeUser(usersURL)
            v_json = json.loads(v)
            self.assertNotEqual(v, None)
            self.assertEqual(v_json["first_name"], q[n].first_name)

    def testValidateUserPostRequest(self):
        for n in xrange(NUM_TESTS):
            req_body = {}
            req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
            req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
            req_body["group"] = randomGroupEnumString()
            result = User.validateUserPostRequest(req_body)
            self.assertEqual(result, True)

    def testFailValidateUserPostRequest_Incomplete(self):
        # Try various incomplete Post Bodies
        for n in xrange(NUM_TESTS):
            req_body = {}
            if (n % 6 == 0):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["group"] = randomGroupEnumString()
            if (n % 6 == 1):
                # req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["group"] = randomGroupEnumString()
            if (n % 6 == 2):
                # req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
            if (n % 6 == 3):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["group"] = randomGroupEnumString()
            if (n % 6 == 4):
                # req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
            if (n % 6 == 5):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()

            result = User.validateUserPostRequest(req_body)
            self.assertEqual(result, False)

    def testFailValidateUserPostRequest_Extra(self):
        # Try various Post Bodies with Extra
        for n in xrange(NUM_TESTS):
            req_body = {}
            req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
            req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
            req_body["group"] = randomGroupEnumString()
            req_body["extra"] = "Extra_Info" + str(n)
            result = User.validateUserPostRequest(req_body)
            self.assertEqual(result, False)

    def testFailValidateUserPostRequest_NullValues(self):
        # Try various Post Bodies None Values
        for n in xrange(NUM_TESTS):
            req_body = {}
            if (n % 3 == 0):
                req_body["first_name"] = None
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
            if (n % 3 == 1):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = None
                req_body["group"] = randomGroupEnumString()
            if (n % 3 == 2):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = None

            result = User.validateUserPostRequest(req_body)
            self.assertEqual(result, False)

    def testValidateUserPatchRequest(self):
        for n in xrange(NUM_TESTS):
            req_body = {}
            if (n % 6 == 0):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
                result = User.validateUserPatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 1):
                # req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
                result = User.validateUserPatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 2):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
                result = User.validateUserPatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 3):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                # req_body["group"] = randomGroupEnumString()
                result = User.validateUserPatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 4):
                req_body["first_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["family_name"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["group"] = randomGroupEnumString()
                req_body["extra"] = "extra" + str(n)
                result = User.validateUserPatchRequest(req_body)
                self.assertEqual(result, False)
            elif (n % 6 == 5):
                result = User.validateUserPatchRequest(req_body)
                self.assertEqual(result, False)
