
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
from const import MAX_STRING_LENGTH, NUM_TESTS, devicesURL
from Device import Device
from Color import Color, randomColorEnumString, randomColorEnum, getColorStringFromEnum
from DeviceModel import DeviceModel, randomDeviceModelEnumString, randomDeviceModelEnum, getDeviceModelStringFromEnum


def GetEntityViaMemcache(entity_key):
    # Get from memcache, then try datastore
    if entity == memcache.get(entity_key):
        return entity

    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


class DeviceDatastoreTestCase( unittest.TestCase ):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        self.v = ValidData()

    def tearDown(self):
        self.testbed.deactivate()

    def testInsertDevice(self):
        for n in xrange(NUM_TESTS):
            device = Device()
            device.color = randomColorEnum()
            device.model = randomDeviceModelEnum()
            device.serial_no = self.v.validRandomString(MAX_STRING_LENGTH)
            device_key = device.put()
            q = Device.query().fetch(n+1)
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, False )

    def testSerializeDevice(self):
        for n in xrange(NUM_TESTS):
            device = Device()
            device.color = randomColorEnum()
            device.model = randomDeviceModelEnum()
            device.serial_no = self.v.validRandomString(MAX_STRING_LENGTH)
            device.is_rented = (n%2==0) # Toggle is_rented
            device_key = device.put()
            q = Device.query().fetch(n+1)
            v_json = q[n].serializeDevice(devicesURL)
            # v_json = json.loads(v)
            self.assertNotEqual(v_json, None)
            self.assertEqual(v_json["id"], device_key.urlsafe())
            self.assertEqual(v_json["color"], getColorStringFromEnum(q[n].color))
            self.assertEqual(v_json["model"], getDeviceModelStringFromEnum(q[n].model))
            self.assertEqual(v_json["is_rented"], q[n].is_rented)


    def testValidateDevicePostRequest(self):
        # for n in xrange(NUM_TESTS):
            n = NUM_TESTS
            req_body = {}
            req_body["color"] = randomColorEnumString()
            req_body["model"] = randomDeviceModelEnumString()
            req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            result = Device.validateDevicePostRequest(req_body)
            self.assertEqual(result, True)

    def testFailValidateDevicePostRequest_Incomplete(self):
        # Try various incomplete Post Bodies
        for n in xrange(NUM_TESTS):
            req_body = {}
            if (n % 6 == 0):
                req_body["color"] = randomColorEnumString()
                # req_body["model"] = randomDeviceModelEnumString()
                # req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 6 == 1):
                # req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                # req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 6 == 2):
                # req_body["color"] = randomColorEnumString()
                # req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 6 == 3):
                # req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 6 == 4):
                req_body["color"] = randomColorEnumString()
                # req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 6 == 5):
                req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                # req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)

            result = Device.validateDevicePostRequest(req_body)
            self.assertEqual(result, False)

    def testFailValidateDevicePostRequest_Extra(self):
        # Try various Post Bodies with Extra
        for n in xrange(NUM_TESTS):
            req_body = {}
            req_body["color"] = randomColorEnumString()
            req_body["model"] = randomDeviceModelEnumString()
            req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            req_body["extra"] = "Extra_Info" + str(n)
            result = Device.validateDevicePostRequest(req_body)
            self.assertEqual(result, False)

    def testFailValidateDevicePostRequest_NullValues(self):
        # Try various Post Bodies None Values
        for n in xrange(NUM_TESTS):
            req_body = {}
            if (n % 3 == 0):
                req_body["color"] = None
                req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 3 == 1):
                req_body["color"] = randomColorEnumString()
                req_body["model"] = None
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 3 == 2):
                req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = None

            result = Device.validateDevicePostRequest(req_body)
            self.assertEqual(result, False)

    def testValidateDevicePatchRequest(self):
        for n in xrange(NUM_TESTS):
            req_body = {}
            if (n % 6 == 0):
                req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
                result = Device.validateDevicePatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 1):
                # req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
                result = Device.validateDevicePatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 2):
                req_body["color"] = randomColorEnumString()
                # req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
                result = Device.validateDevicePatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 3):
                req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                # req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
                result = Device.validateDevicePatchRequest(req_body)
                self.assertEqual(result, True)
            elif (n % 6 == 4):
                req_body["color"] = randomColorEnumString()
                req_body["model"] = randomDeviceModelEnumString()
                req_body["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
                req_body["extra"] = "extra" + str(n)
                result = Device.validateDevicePatchRequest(req_body)
                self.assertEqual(result, False)
            elif (n % 6 == 5):
                result = Device.validateDevicePatchRequest(req_body)
                self.assertEqual(result, False)
