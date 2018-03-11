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

import unittest
import webtest
import webapp2
from webapp2 import Route
from datetime import datetime

from RentalHandler import RentalHandler
from UserHandler import UserHandler, UsersHandler
from DeviceHandler import DeviceHandler, DevicesHandler
from webapp2_extras.routes import RedirectRoute, PathPrefixRoute

from randomData import ValidData
from const import MAX_STRING_LENGTH, NUM_TESTS, baseURL, devicesPath, devicesURL, usersPath, usersURL
from Device import Device
from User import User
from Group import randomGroupEnumString, randomGroupEnum
from Color import randomColorEnumString, randomColorEnum
from DeviceModel import randomDeviceModelEnumString, randomDeviceModelEnum


class RentalAPITestCase( unittest.TestCase ):
    def setUp(self):
        allowed_methods = webapp2.WSGIApplication.allowed_methods
        new_allowed_methods = allowed_methods.union(('PATCH',))
        webapp2.WSGIApplication.allowed_methods = new_allowed_methods
        app = webapp2.WSGIApplication([
            Route('/users', handler=UsersHandler, name='users'),
            PathPrefixRoute( '/users',[
                Route('/', handler=UsersHandler, name='users'),
                Route('/<user_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=UserHandler, name='user'),

                Route('/<user_id:([A-Z]|[a-z]|[0-9]|[-._])+>/devices/<device_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=RentalHandler, name='rental'),

            ]),
            Route('/devices', handler=DevicesHandler, name='devices'),
            PathPrefixRoute( '/devices',[
                Route('/', handler=DevicesHandler, name='devices'),
                Route('/<device_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=DeviceHandler, name='device'),

                Route('/<device_id:([A-Z]|[a-z]|[0-9]|[-._])+>/users/<user_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=RentalHandler, name='rental'),
            ]),
        ])
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

    def testRentalHandlerCheckOut(self):
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
            user_id = q[n].key.urlsafe()
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

            # Add Device to User via PUT
            if (n %2 == 0):
                url = baseURL
                url += usersPath + "/" + user_id + devicesPath + "/" + device_id
            elif (n %2 == 1):
                url = baseURL
                url += devicesPath + "/" + device_id + usersPath + "/" + user_id

            response = self.testapp.put(url)

            # Check Return
            self.assertEqual(response.status_int, 204)

            # Test Changes Occurred
            # Verify User has device ID
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, user.device_id)
            self.assertEqual(q[n].device_id, device_id)
            self.assertNotEqual(q[n].start_datetime, None)

            # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )

    def testRentalHandlerCheckOutError(self):
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
            user_id = q[n].key.urlsafe()
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

            # Add Device to User via PUT
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id

            response = self.testapp.put(url)

            # Check Return
            self.assertEqual(response.status_int, 204)

            # Test Changes Occurred
            # Verify User has device ID
            q1 = User.query().fetch(n+1)
            self.assertEqual(q1[n].first_name, user.first_name)
            self.assertEqual(q1[n].family_name, user.family_name)
            self.assertEqual(q1[n].group, user.group)
            self.assertEqual(q1[n].device_id, user.device_id)
            self.assertEqual(q1[n].device_id, device_id)
            self.assertNotEqual(q1[n].start_datetime, None)

            # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )

            # Add Try to RE-CHECK OUT Device to User via PUT, get same result
            response = self.testapp.put(url)

            # Check Return
            self.assertEqual(response.status_int, 204)
            # Test Changes DID NOT Occurred after re-attempt
            # Verify User stll has device ID
            q2 = User.query().fetch(n+1)
            self.assertEqual(q2[n].first_name, q1[n].first_name)
            self.assertEqual(q2[n].family_name,q1[n].family_name)
            self.assertEqual(q2[n].group, q1[n].group)
            self.assertEqual(q2[n].device_id, q1[n].device_id)
            self.assertEqual(q2[n].start_datetime, q1[n].start_datetime)

            # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )

            # Add INVALID Device to User via PUT, get error
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id + "1"

            response = self.testapp.put(url, expect_errors=True)

            # Check Return
            self.assertEqual(response.status_int, 400)
            q3 = User.query().fetch(n+1)
            self.assertEqual(q2[n].first_name, q3[n].first_name)
            self.assertEqual(q2[n].family_name,q3[n].family_name)
            self.assertEqual(q2[n].group, q3[n].group)
            self.assertEqual(q2[n].device_id, q3[n].device_id)
            self.assertEqual(q2[n].start_datetime, q3[n].start_datetime)

            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )


    def testRentalHandlerCheckIn(self):
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
            user_id = q[n].key.urlsafe()
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

            # Add Device to User via PUT
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id

            response = self.testapp.put(url)

            # Check Return
            self.assertEqual(response.status_int, 204)

            # Test Changes Occurred
            # Verify User has device ID
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, user.device_id)
            self.assertEqual(q[n].device_id, device_id)
            self.assertNotEqual(q[n].start_datetime, None)

            # # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )

            # REMOVE Device to User via DELETE
            response = self.testapp.delete(url)

            # Check Return
            self.assertEqual(response.status_int, 204)

            # Test Changes Occurred
            # Verify User has None for device ID, start_datetime
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, None)
            self.assertEqual(q[n].start_datetime, None)

            # # Verify Device is NOT rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, False )



    def testRentalHandlerCheckInError(self):
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
            user_id = q[n].key.urlsafe()
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

            # Add Device to User via PUT
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id

            response = self.testapp.put(url)

            # Check Return
            self.assertEqual(response.status_int, 204)

            # Test Changes Occurred
            # Verify User has device ID
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, user.first_name)
            self.assertEqual(q[n].family_name, user.family_name)
            self.assertEqual(q[n].group, user.group)
            self.assertEqual(q[n].device_id, user.device_id)
            self.assertEqual(q[n].device_id, device_id)
            self.assertNotEqual(q[n].start_datetime, None)

            # # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(q[n].color, device.color)
            self.assertEqual(q[n].model, device.model)
            self.assertEqual(q[n].serial_no, device.serial_no)
            self.assertEqual(q[n].is_rented, True )

            # FAIL to REMOVE Different Device from User via DELETE
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id
            url += "2"
            response = self.testapp.delete(url, expect_errors=True)

            # Check Return
            self.assertEqual(response.status_int, 404)

            # Add INVALID Device to User via PUT, get error
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id + "1"

            response = self.testapp.put(url, expect_errors=True)

            # Check Return
            self.assertEqual(response.status_int, 400)
