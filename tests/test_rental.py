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
from datetime import datetime
from const import MAX_STRING_LENGTH, NUM_TESTS, usersURL, devicesURL
from User import User
from Device import Device
from Group import Group, randomGroupEnum, randomGroupEnumString
from Color import Color, randomColorEnum, randomColorEnumString
from DeviceModel import DeviceModel, randomDeviceModelEnum, randomDeviceModelEnumString


def GetEntityViaMemcache(entity_key):
    # Get from memcache, then try datastore
    if entity == memcache.get(entity_key):
        return entity

    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


class RentalDatastoreTestCase( unittest.TestCase ):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        self.v = ValidData()

    def tearDown(self):
        self.testbed.deactivate()

    def testRentalCheckOut(self):
        for n in xrange(NUM_TESTS):
            # Create User
            user = User()
            user.first_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.family_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.group = randomGroupEnum()
            user.device_id = None
            user.start_datetime = None
            user_key = user.put()

            # Verify User has no device
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, user.device_id)
            self.assertEqual(q[n].start_datetime, user.start_datetime)

            # Create Device
            device = Device()
            device.color = randomColorEnum()
            device.model = randomDeviceModelEnum()
            device.serial_no = self.v.validRandomString(MAX_STRING_LENGTH)
            device_key = device.put()

            # Verify Device is not rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, False )

            # Add Device to User
            start_datetime = datetime.now()
            result = user.checkOutDevice(device_id, start_datetime)

            self.assertNotEqual(result, None)

            # Verify User has device ID
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, user.device_id)
            self.assertEqual(q[n].device_id, device_id)
            self.assertEqual(q[n].start_datetime, user.start_datetime)
            self.assertEqual(q[n].start_datetime, start_datetime)

            # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )

    def testRentalCheckOutFails(self):
        for n in xrange(NUM_TESTS):
            # Create User
            user = User()
            user.first_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.family_name = self.v.validRandomString(MAX_STRING_LENGTH)
            user.group = randomGroupEnum()
            user.device_id = None
            user.start_datetime = None
            user_key = user.put()

            # Verify User has no device
            u = User.query().fetch(n+1)
            self.assertEqual(u[n].first_name, user.first_name)
            self.assertEqual(u[n].family_name, user.family_name)
            self.assertEqual(u[n].group, user.group)
            self.assertEqual(u[n].device_id, user.device_id)
            self.assertEqual(u[n].start_datetime, user.start_datetime)

            # Create Device
            device = Device()
            device.color = randomColorEnum()
            device.model = randomDeviceModelEnum()
            device.serial_no = self.v.validRandomString(MAX_STRING_LENGTH)
            device_key = device.put()

            # Verify Device is not rented
            d = Device.query().fetch(n+1)
            device_id = d[n].key.urlsafe()
            self.assertEqual(d[n].color, device.color)
            self.assertEqual(d[n].model, device.model)
            self.assertEqual(d[n].serial_no, device.serial_no)
            self.assertEqual(d[n].is_rented, False )

            if (n % 2 == 0):
                # Set Device to unavailable
                d[n].is_rented = True
                d[n].put()
            elif (n % 2 == 1):
                # Set User to another device
                u[n].device_id = "random_device_id"
                u[n].start_datetime = datetime.now()
                u[n].put()

            # Add Device to User
            start_datetime = datetime.now()
            result = user.checkOutDevice(device_id, start_datetime)

            self.assertEqual(result, None)

            # Verify User is unchanged
            u2 = User.query().fetch(n+1)
            self.assertEqual(u2[n].first_name, u[n].first_name)
            self.assertEqual(u2[n].family_name, u[n].family_name)
            self.assertEqual(u2[n].group, u[n].group)
            self.assertEqual(u2[n].device_id, u[n].device_id)
            self.assertEqual(u2[n].start_datetime, u[n].start_datetime)

            # Verify Device is unchanged
            d2 = Device.query().fetch(n+1)
            device_id = d2[n].key.urlsafe()
            self.assertEqual(d2[n].color, d[n].color)
            self.assertEqual(d2[n].model, d[n].model)
            self.assertEqual(d2[n].serial_no, d[n].serial_no)
            self.assertEqual(d2[n].is_rented, d[n].is_rented )
