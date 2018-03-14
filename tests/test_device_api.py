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
from DeviceHandler import DevicesHandler, DeviceHandler
from UserHandler import UsersHandler, UserHandler
from RentalHandler import RentalHandler
from webapp2_extras.routes import RedirectRoute, PathPrefixRoute

from randomData import ValidData
from const import MAX_STRING_LENGTH, NUM_TESTS, devicesPath, devicesURL, usersPath, usersURL, baseURL
from User import User
from Device import Device
from Group import randomGroupEnumString
from Color import randomColorEnumString
from DeviceModel import randomDeviceModelEnumString


class DeviceAPITestCase( unittest.TestCase ):
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

    def testDevicesHandlerPost_Return(self):
        for n in xrange(NUM_TESTS):
            # Create
            url = devicesURL
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString(MAX_STRING_LENGTH)
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)

            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)

    def testPostDeviceReturnsError(self):
        for n in xrange(NUM_TESTS):
            url = devicesURL
            data = {}
            if (n % 11) == 0:
                # data["color"] = randomColorEnumString(),
                data["model"] = randomDeviceModelEnumString(),
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 1:
                data["color"] = randomColorEnumString(),
                # data["model"] = randomDeviceModelEnumString(),
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 2:
                # Create
                data["color"] = randomColorEnumString(),
                data["model"] = randomDeviceModelEnumString(),
                # data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 3:
                # data["color"] = randomColorEnumString(),
                # data["model"] = randomDeviceModelEnumString(),
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 4:
                data["color"] = randomColorEnumString(),
                # data["model"] = randomDeviceModelEnumString(),
                # data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 5:
                # Create
                # data["color"] = randomColorEnumString(),
                data["model"] = randomDeviceModelEnumString(),
                # data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 6:
                # Create
                data["color"] = "wrong_color",
                data["model"] = randomDeviceModelEnumString(),
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 7:
                # Create
                data["color"] = randomColorEnumString(),
                data["model"] = None
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 8:
                # Create
                data["color"] = None,
                data["model"] = randomDeviceModelEnumString(),
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
            if (n % 11) == 9:
                # Create
                data["color"] = randomColorEnumString(),
                data["model"] = randomDeviceModelEnumString(),
                data["serial_no"] = self.v.validRandomString(MAX_STRING_LENGTH)
                data["extra"] = "Extra" + str(n);
            if (n % 11) == 10:
                data = {}

            # Check Return
            response = self.testapp.post_json(devicesPath, data, expect_errors=True)

            # Check Return
            status_int = response.status_int
            self.assertEqual(status_int, 400)

            payload = response.json

            # payload = json.loads(res.content)
            self.assertEqual("error" in payload.keys(), True)
            self.assertEqual("id" in payload.keys(), False)
            self.assertEqual("url" in payload.keys(), False)
            self.assertEqual("model" in payload.keys(), False)
            self.assertEqual("color" in payload.keys(), False)
            self.assertEqual("serial_no" in payload.keys(), False)
            self.assertEqual("is_rented" in payload.keys(), False)

    def testPostDeviceIsAddedToDatastore(self):
        # Post Device and ensure it is added to Datastore GET ALL
        for n in xrange(NUM_TESTS):
            url = devicesURL
            # PRE: GET ALL Devices
            response = self.testapp.get(devicesURL);
            pre_payload = response.json
            self.assertEqual(type(pre_payload), list);
            for i in pre_payload:
                # obj = json.loads(i)
                obj = i
                self.assertEqual(type(obj), dict)
                self.assertEqual('error' in obj.keys(), False)
                self.assertEqual('url' in obj.keys(), True)
                self.assertEqual('id' in obj.keys(), True)
                self.assertEqual("id" in payload.keys(), True)
                self.assertEqual("url" in payload.keys(), True)
                device_id = payload["id"]
                self.assertEqual(payload['url'], devicesURL + "/" + device_id)
                self.assertEqual('color' in obj.keys(), True)
                self.assertEqual('model' in obj.keys(), True)
                self.assertEqual('serial_no' in obj.keys(), True)


            # Add New
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString( MAX_STRING_LENGTH )
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            self.assertEqual("color" in payload.keys(), True)
            self.assertEqual("model" in payload.keys(), True)
            self.assertEqual("serial_no" in payload.keys(), True)
            self.assertEqual("is_rented" in payload.keys(), True)
            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            # Check Object added to GET ALL
            # AFTER: GET ALL Devices
            response = self.testapp.get(devicesURL);
            post_payload = response.json
            self.assertEqual(type(post_payload), list);
            for i in xrange(len(post_payload)):
                # obj = json.loads(post_payload[i])
                obj = post_payload[i]
                self.assertEqual(type(obj), dict)
                self.assertEqual('error' in obj.keys(), False)
                self.assertEqual('color' in obj.keys(), True)
                self.assertEqual('model' in obj.keys(), True)
                self.assertEqual('serial_no' in obj.keys(), True)
                self.assertEqual('is_rented' in obj.keys(), True)
                if i < len(pre_payload):
                    # pre_obj = json.loads(pre_payload[i])
                    pre_obj = pre_payload[i]
                    self.assertEqual(pre_obj['color'], obj['color'])
                    self.assertEqual(pre_obj['model'], obj['model'])
                    self.assertEqual(pre_obj['serial_no'], obj['serial_no'])
                    self.assertEqual(pre_obj['is_rented'], obj['is_rented'])
                else:
                    # compare posted object to this one
                    self.assertEqual(data['color'], obj['color'])
                    self.assertEqual(data['model'], obj['model'])
                    self.assertEqual(data['serial_no'], obj['serial_no'])
                    self.assertEqual(False, obj['is_rented'])

    def testGetDeviceInDatastore(self):
        # Post Device and ensure it is added to Datastore GET ONE
        for n in xrange(NUM_TESTS):
            url = devicesURL
            # Add New
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString( MAX_STRING_LENGTH )
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            self.assertEqual("color" in payload.keys(), True)
            self.assertEqual("model" in payload.keys(), True)
            self.assertEqual("serial_no" in payload.keys(), True)
            self.assertEqual("is_rented" in payload.keys(), True)
            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Devices via payload['url']
            response = self.testapp.get(payload['url']);
            obj = response.json
            # obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual('id' in obj.keys(), True)
            self.assertEqual('url' in obj.keys(), True)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)
            self.assertEqual('color' in obj.keys(), True)
            self.assertEqual('model' in obj.keys(), True)
            self.assertEqual('serial_no' in obj.keys(), True)
            self.assertEqual('is_rented' in obj.keys(), True)
            self.assertEqual(data['color'], obj['color'])
            self.assertEqual(data['model'], obj['model'])
            self.assertEqual(data['serial_no'], obj['serial_no'])
            self.assertEqual(False, obj['is_rented'])

    def testEditDevicesInDatastore(self):
        for n in xrange(NUM_TESTS):
            url = devicesURL
            # Add New
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString(MAX_STRING_LENGTH)
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            self.assertEqual("color" in payload.keys(), True)
            self.assertEqual("model" in payload.keys(), True)
            self.assertEqual("serial_no" in payload.keys(), True)
            self.assertEqual("is_rented" in payload.keys(), True)
            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Devices via payload['url']
            response = self.testapp.get(payload['url']);
            obj = response.json
            # obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in obj.keys(), True)
            self.assertEqual("url" in obj.keys(), True)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)
            self.assertEqual('color' in obj.keys(), True)
            self.assertEqual('model' in obj.keys(), True)
            self.assertEqual('serial_no' in obj.keys(), True)
            self.assertEqual('is_rented' in obj.keys(), True)
            self.assertEqual(data['color'], obj['color'])
            self.assertEqual(data['model'], obj['model'])
            self.assertEqual(data['serial_no'], obj['serial_no'])
            self.assertEqual(False, obj['is_rented'])

            # Edit Object
            obj_new = {}
            obj_new["color"] = obj["color"]
            obj_new["model"] = obj["model"]
            obj_new["serial_no"] = obj["serial_no"]

            if (n % 3 == 0):
                obj_new["color"] = randomColorEnumString()
            elif (n % 3 == 1):
                obj_new["model"] = randomDeviceModelEnumString()
            elif (n % 3 == 2):
                obj_new["serial_no"] = self.v.validRandomString( MAX_STRING_LENGTH )

            response = self.testapp.patch_json(payload['url'], obj_new)

            # Check Object changed
            response = self.testapp.get(payload['url']);
            obj2 = response.json
            # obj2 = json.loads(post_payload)
            self.assertEqual('error' in obj2.keys(), False)
            self.assertEqual("id" in obj2.keys(), True)
            self.assertEqual("url" in obj2.keys(), True)
            device_id = obj2["id"]
            self.assertEqual(obj2['url'], devicesURL + "/" + device_id)

            self.assertEqual('color' in obj2.keys(), True)
            self.assertEqual('model' in obj2.keys(), True)
            self.assertEqual('serial_no' in obj2.keys(), True)
            self.assertEqual('is_rented' in obj2.keys(), True)
            self.assertEqual(obj_new['color'], obj2['color'])
            self.assertEqual(obj_new['model'], obj2['model'])
            self.assertEqual(obj_new['serial_no'], obj2['serial_no'])
            self.assertEqual(False, obj2['is_rented'])

            if (n % 3 == 0):
                self.assertNotEqual(data['color'], json.dumps(obj2['color']))
            elif (n % 3 == 1):
                self.assertNotEqual(data['model'], json.dumps(obj2['model']))
            elif (n % 3 == 2):
                self.assertNotEqual(data['serial_no'], json.dumps(obj2['serial_no']))

            return

    def testEditDevicesInDatastoreError(self):
        # Too much info
        # No Changes
        for n in xrange(NUM_TESTS):
            url = devicesURL
            # Add New
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString(MAX_STRING_LENGTH)
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            self.assertEqual("color" in payload.keys(), True)
            self.assertEqual("model" in payload.keys(), True)
            self.assertEqual("serial_no" in payload.keys(), True)
            self.assertEqual("is_rented" in payload.keys(), True)
            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Devices via payload['url']
            response = self.testapp.get(payload['url']);
            obj = response.json
            # obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in obj.keys(), True)
            self.assertEqual("url" in obj.keys(), True)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)
            self.assertEqual('color' in obj.keys(), True)
            self.assertEqual('model' in obj.keys(), True)
            self.assertEqual('serial_no' in obj.keys(), True)
            self.assertEqual('is_rented' in obj.keys(), True)
            self.assertEqual(data['color'], obj['color'])
            self.assertEqual(data['model'], obj['model'])
            self.assertEqual(data['serial_no'], obj['serial_no'])
            self.assertEqual(False, obj['is_rented'])

            # Edit Object Invalid
            obj_new = {}
            obj_new["color"] = obj["color"]
            obj_new["model"] = obj["model"]
            obj_new["serial_no"] = obj["serial_no"]

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
            obj2 = response.json
            # obj2 = json.loads(post_payload)
            self.assertEqual('error' in obj2.keys(), False  )
            self.assertEqual("id" in obj2.keys(), True)
            self.assertEqual("url" in obj2.keys(), True)
            device_id = payload["id"]
            self.assertEqual(obj2['url'], devicesURL + "/" + device_id)
            self.assertEqual('color' in obj2.keys(), True)
            self.assertEqual('model' in obj2.keys(), True)
            self.assertEqual('serial_no' in obj2.keys(), True)
            self.assertEqual('is_rented' in obj2.keys(), True)
            self.assertEqual(data['color'], obj2['color'])
            self.assertEqual(data['model'], obj2['model'])
            self.assertEqual(data['serial_no'], obj2['serial_no'])
            self.assertEqual(False, obj2['is_rented'])
            return

    def testDeleteDevicesInDatastore(self):
        # Create, Verify, Delete Verify
        for n in xrange(NUM_TESTS):
            url = devicesURL
            # Add New
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString(MAX_STRING_LENGTH)
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            self.assertEqual("color" in payload.keys(), True)
            self.assertEqual("model" in payload.keys(), True)
            self.assertEqual("serial_no" in payload.keys(), True)
            self.assertEqual("is_rented" in payload.keys(), True)
            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Devices via payload['url']
            response = self.testapp.get(payload['url']);
            obj = response.json
            # obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in obj.keys(), True)
            self.assertEqual("url" in obj.keys(), True)
            self.assertEqual('color' in obj.keys(), True)
            self.assertEqual('model' in obj.keys(), True)
            self.assertEqual('serial_no' in obj.keys(), True)
            self.assertEqual('is_rented' in obj.keys(), True)
            self.assertEqual(data['color'], obj['color'])
            self.assertEqual(data['model'], obj['model'])
            self.assertEqual(data['serial_no'], obj['serial_no'])
            self.assertEqual(False, obj['is_rented'])

            # Delete Object
            response = self.testapp.delete(payload['url'])
            self.assertEqual(response.status_int, 204)

            # Check Object Not there
            response = self.testapp.get(payload['url'], expect_errors=True);
            self.assertEqual(response.status_int, 404)

    def testDeleteDevicesInDatastoreFAIL(self):
        # Create, Verify, Check out Device, refuse Delete Verify
        for n in xrange(NUM_TESTS):
            url = devicesURL
            # Add New
            data = {
                "color": randomColorEnumString(),
                "model": randomDeviceModelEnumString(),
                "serial_no": self.v.validRandomString(MAX_STRING_LENGTH)
            }
            response = self.testapp.post_json(devicesPath, data)

            # Check Return
            payload = response.json
            self.assertEqual("error" in payload.keys(), False)
            self.assertEqual("id" in payload.keys(), True)
            self.assertEqual("url" in payload.keys(), True)
            self.assertEqual("color" in payload.keys(), True)
            self.assertEqual("model" in payload.keys(), True)
            self.assertEqual("serial_no" in payload.keys(), True)
            self.assertEqual("is_rented" in payload.keys(), True)
            self.assertEqual(payload['color'], data["color"])
            self.assertEqual(payload['model'], data["model"])
            self.assertEqual(payload['serial_no'], data["serial_no"])
            self.assertEqual(payload['is_rented'], False)
            device_id = payload["id"]
            self.assertEqual(payload['url'], devicesURL + "/" + device_id)

            # Check Object added to GET 1
            # AFTER: GET ONE Devices via payload['url']
            response = self.testapp.get(payload['url']);
            obj = response.json
            # obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in obj.keys(), True)
            self.assertEqual("url" in obj.keys(), True)
            self.assertEqual('color' in obj.keys(), True)
            self.assertEqual('model' in obj.keys(), True)
            self.assertEqual('serial_no' in obj.keys(), True)
            self.assertEqual('is_rented' in obj.keys(), True)
            self.assertEqual(data['color'], obj['color'])
            self.assertEqual(data['model'], obj['model'])
            self.assertEqual(data['serial_no'], obj['serial_no'])
            self.assertEqual(False, obj['is_rented'])

            # Add New
            data2 = {
                "first_name": self.v.validRandomString( MAX_STRING_LENGTH ),
                "family_name": self.v.validRandomString( MAX_STRING_LENGTH ),
                "group": randomGroupEnumString()
            }
            response = self.testapp.post_json(usersPath, data2)

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

            self.assertEqual(payload['first_name'], data2["first_name"])
            self.assertEqual(payload['family_name'], data2["family_name"])
            self.assertEqual(payload['group'], data2["group"])
            self.assertEqual(payload['device_id'], None)
            self.assertEqual(payload['start_datetime'], None)
            user_id = payload["id"]
            self.assertEqual(payload['url'], usersURL + "/" + user_id)


            # Check out device
            url = baseURL
            url += usersPath + "/" + user_id + devicesPath + "/" + device_id

            response = self.testapp.put(url)

            # Check Return
            self.assertEqual(response.status_int, 204)

            # Test Changes Occurred
            # Verify User has device ID
            q = User.query().fetch(n+1)
            self.assertEqual(q[n].first_name, data2["first_name"])
            self.assertEqual(q[n].family_name, data2["family_name"])
            self.assertEqual(str(q[n].group), data2["group"])
            self.assertEqual(q[n].device_id, device_id)
            self.assertNotEqual(q[n].start_datetime, None)
            start_datetime = q[n].start_datetime

            # Verify Device is rented
            q = Device.query().fetch(n+1)
            device_id = q[n].key.urlsafe()
            self.assertEqual(str(q[n].color), data["color"])
            self.assertEqual(str(q[n].model), data["model"])
            self.assertEqual(q[n].serial_no, data["serial_no"])
            self.assertEqual(q[n].is_rented, True )

            # TRY TO DELETE DEVICE
            url = devicesURL + "/" + device_id
            response = self.testapp.delete(url, expect_errors=True)
            self.assertEqual(response.status_int, 400)

            # Check DEVICE IS still there
            # Check Object added to GET 1
            # AFTER: GET ONE Users via payload['url']
            response = self.testapp.get(url);
            obj = response.json
            # obj = json.loads(post_payload)
            self.assertEqual('error' in obj.keys(), False)
            self.assertEqual("id" in obj.keys(), True)
            self.assertEqual("url" in obj.keys(), True)
            self.assertEqual('color' in obj.keys(), True)
            self.assertEqual('model' in obj.keys(), True)
            self.assertEqual('serial_no' in obj.keys(), True)
            self.assertEqual('is_rented' in obj.keys(), True)
            self.assertEqual(data['color'], obj['color'])
            self.assertEqual(data['model'], obj['model'])
            self.assertEqual(data['serial_no'], obj['serial_no'])
            self.assertEqual(True, obj['is_rented'])
