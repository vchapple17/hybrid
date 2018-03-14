#!/usr/bin/env python
import sys
sys.path.append("./models/")

from webapp2 import RequestHandler
import webapp2_extras
import json
from google.appengine.ext import ndb
from datetime import datetime
from const import baseURL, devicesURL
from Device import Device
from DeviceModel import getDeviceModelEnumFromString
from Color import getColorEnumFromString

class DevicesHandler(RequestHandler):
    def get(self):
        print("DevicesHandler: GET LIST")
        # Retrieve boats
        devices = Device.query().fetch()

        # Send response
        res = []
        for device in devices:
            obj = device.serializeDevice( devicesURL );
            res.append(obj)
        # self.response.content_type = 'text/plain'
        self.response.headers.add('Content-Type', "application/json")
        self.response.status_int = 200;
        self.response.out.write(json.dumps(res))
        return

    def post(self):
        print("DevicesHandler: CREATE POST")
        # Save Request Body
        try:
            req = self.request.body
            obj = json.loads(req)

            if (Device.validateDevicePostRequest( obj )):
                color_enum = getColorEnumFromString(obj["color"])
                model_enum = getDeviceModelEnumFromString(obj["model"])
                serial_no = obj["serial_no"]
                # Device req contains exactly what is required
                device = Device( color=color_enum, model=model_enum, serial_no=serial_no)
                device.put()
            else:
                raise TypeError
        except(TypeError):
            self.response.write(json.dumps({"error": "Invalid Data"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return
        except:
            # print(obj)
            self.response.write(json.dumps({"error": "Cannot save entity"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return

        # Send response
        try:
            self.response.content_type = 'application/json'
            self.response.status_int = 201;
            self.response.write( json.dumps(device.serializeDevice(devicesURL)) )
        except:
            self.response.write(json.dumps({"error": "Cannot write response."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 500;
            return

# Device identified by id
class DeviceHandler(RequestHandler):
    def get(self, device_id):
        print("DeviceHandler: GET 1: " + device_id)
        # Convert boat_id to ndb object
        try:
            device_key = ndb.Key(urlsafe=device_id);
            device = device_key.get()
            if (device == None):
                raise TypeError;
        except:
            self.response.write(json.dumps({"error": "Error getting device"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return

        # Send response
        res = device.serializeDevice( devicesURL );
        # deviceURL = devicesURL + "/" + device_id;
        self.response.content_type = 'application/json'
        self.response.status_int = 200;
        self.response.write(json.dumps(res))

    def patch(self, device_id):
        print("DeviceHandler: PATCH")

        try:
            # Convert boat_id to ndb object
            device_key = ndb.Key(urlsafe=device_id);
            device = device_key.get()
            if (device == None):
                print("DeviceHandler: Device is of type None")
                raise TypeError("Device is of type None")
        except:
            self.response.write(json.dumps({"error": "Invalid Device ID"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return;
        # Get json from Request Body
        try:
            req = self.request.body;
            obj = json.loads(req);
            if (Device.validateDevicePatchRequest( obj )):
                # Device req contains exactly what is required
                # Submit Patch
                if (obj["color"] != None):
                    device.color = getColorEnumFromString(obj["color"])
                if (obj["model"] != None):
                    device.model = getDeviceModelEnumFromString(obj["model"])
                if (obj["serial_no"] != None):
                    device.serial_no = obj["serial_no"]
                device.put()
            else:
                print("DeviceHandler: invalid")
                raise TypeError
        except(TypeError):
            print({"error": "Invalid inputs"})
            self.response.write(json.dumps({"error": "Invalid inputs"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return
        except:
            self.response.write(json.dumps({"error": "Cannot save entity"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return

        # Send response
        try:
            self.response.content_type = 'application/json'
            self.response.status_int = 201;
            self.response.write( json.dumps(device.serializeDevice(devicesURL)))
            return
        except:
            self.response.write(json.dumps({"error": "Cannot write response."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 500;
            return

    def delete(self, device_id):
        print("DeviceHandler: DELETE 1")

        # Convert device_id to ndb KEY
        try:
            device_key = ndb.Key(urlsafe=device_id);
            device = device_key.get()
            if (device == None):
                raise TypeError
        except:
            self.response.content_type = None
            self.response.status_int = 204
            return

        if (device.canDelete() == False):
            self.response.status_int = 400
            return

        # Delete boat entity
        try:
            device_key.delete();
        except:
            self.response.write(json.dumps({"error": "Cannot delete entity."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return

        # # Send response that boat is deleted
        self.response.status_int = 204;
        self.response.content_type = None;
        return;
