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
from User import User
from DeviceModel import getDeviceModelEnumFromString
from Color import getColorEnumFromString

class RentalHandler(RequestHandler):
    def put(self, user_id, device_id):
        print("RentingHandler: Check Out ")
        # Convert user_id to ndb object
        try:
            user_key = ndb.Key(urlsafe=user_id);
            user = user_key.get()
            if (user == None):
                raise TypeError;
        except:
            self.response.write(json.dumps({"error": "Error getting user"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return

        try:
            # rent device to user
            if (user.checkOutDevice(device_id, datetime.now()) == None):
                raise TypeError
        except(TypeError):
            self.response.write(json.dumps({"error": "Error checking out device"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return
        except:
            self.response.write(json.dumps({"error": "Error checking out device"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 500;
            return

        # Send response
        self.response.content_type = None
        self.response.status_int = 204;
        # self.response.write(json.dumps(res))

    def delete(self, user_id, device_id):
        print("RentalHandler: DELETE: check in Device");
        # Convert boat_id and slip_id to ndb objects
        try:
            user_key = ndb.Key(urlsafe=user_id);
            user = user_key.get()
            if (user == None):
                raise TypeError
        except:
            self.response.write(json.dumps({"error": "Invalid user inputs"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return

        try:
            device_key = ndb.Key(urlsafe=device_id);
            device = device_key.get()
            if (device == None):
                raise TypeError
        except:
            self.response.write(json.dumps({"error": "Invalid device inputs"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return

        if ( user.checkInDevice(device_id) == None ):
            # Send Response
            self.response.write(json.dumps({"error": "Cannot check in device."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return

        # Send response
        self.response.content_type = None
        self.response.status_int = 204;
