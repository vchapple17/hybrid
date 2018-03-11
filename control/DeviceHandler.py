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
            self.response.write( device.serializeDevice(devicesURL) )
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
            self.response.write( device.serializeDevice(devicesURL) )
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
            self.response.status_int = 204;
            return


        # occupied_slip
    #     try:
    #         # Find Boat's Slip and Remove
    #         query = Slip.query()
    #         slips = query.filter(Slip._properties["current_boat"] == boat_id).fetch()
    #
    #         if (len(slips) == 1):
    #             slip = slips[0];
    #
    #             # Backup Boat URL and ID for Slip
    #             boatURL = slip.current_boat_url
    #             boatDate = slip.arrival_date
    #
    #             # Update Slip
    #             slip.current_boat = None;
    #             slip.current_boat_url = None;
    #             slip.arrival_date = None;
    #
    #             slip.put()
    #             print("UPDATED SLIP", slip)
    #     except:
    #         # Send Response
    #         self.response.write(json.dumps({"error": "Cannot update slip."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 500;
    #         return
    #
        # Delete boat entity
        try:
            device_key.delete();
        except:
            self.response.write(json.dumps({"error": "Cannot delete entity."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            #
            # slip.current_boat = boat_id;
            # slip.current_boat_url = boatURL;
            # slip.arrival_date = boatDate;
            # slip.put()
            return

        # # Send response that boat is deleted
        self.response.status_int = 204;
        self.response.content_type = None;
        return;


# class DockingHandler(RequestHandler):
    # def put(self, boat_id, slip_id):
    #     print("DockingHandler: PUT: Boat to Slip");
    #     # Add Boat URL, Boat ID, and Arrival Date to Slip
    #
    #     # Convert boat_id and slip_id to ndb objects
    #     try:
    #         boat_key = ndb.Key(urlsafe=boat_id);
    #         boat = boat_key.get()
    #         if (boat == None):
    #             raise TypeError("Boat is of type none")
    #         boatURL = boatsURL + "/" + boat_id;
    #     except:
    #         self.response.write(json.dumps({"error": "Invalid inputs"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 404;
    #         return
    #
    #     try:
    #         slip_key = ndb.Key(urlsafe=slip_id);
    #         slip = slip_key.get()
    #         if (slip == None):
    #             raise TypeError("Slip is of type none")
    #     except:
    #         # print("boat", boat);
    #         self.response.write(json.dumps({"error": "Invalid inputs"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 404;
    #         return
    #
    #     # Verify Boat At Sea, reject if not
    #     if (boat.at_sea == False):
    #         # print("boat", boat);
    #         self.response.write(json.dumps({"error": "Boat already docked."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 403;
    #         return
    #
    #     # Verify Slip Empty, reject if not
    #     if (slip.current_boat != None) or (slip.current_boat_url != None) or (slip.arrival_date != None):
    #         self.response.write(json.dumps({"error": "Slip already occupied."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 403;
    #         return
    #
    #
    #     # Get json from Request Body
    #     try:
    #         req = self.request.body;
    #         obj = json.loads(req);
    #     except:
    #         self.response.write(json.dumps({"error": "Invalid Request."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Iterate through each json Key before saving
    #     try:
    #         saveObject = False;     # Update to True if new information given
    #         for key in obj:
    #             # Check that key is a valid input
    #             if (key == "arrival_date"):
    #                 datestring = str(obj["arrival_date"]);
    #                 slip.arrival_date = datetime.strptime(datestring, "%m/%d/%Y").date();
    #                 # slip.arrival_date = datestring;
    #                 saveObject = True;
    #             else:
    #                 saveObject = False;
    #                 # Invalid Information Given in json
    #                 self.response.write(json.dumps({"error": "Invalid Request."}));
    #                 self.response.headers.add('Content-Type', "application/json");
    #                 self.response.status_int = 400;
    #                 return
    #     except (TypeError, ValueError):
    #         self.response.write(json.dumps({"error": "Invalid Request."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Save new boat info to slip if saveObject = True
    #     try:
    #         if (saveObject == False):
    #             self.response.write(json.dumps({"error": "Invalid Request."}));
    #             self.response.headers.add('Content-Type', "application/json");
    #             self.response.status_int = 400;
    #             return
    #         else:
    #             slip.current_boat = boat_id
    #             slip.current_boat_url = boatURL
    #             slip.put()
    #     except:
    #         self.response.write(json.dumps({"error": "Error docking boat."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 500;
    #         return
    #
    #     # Update Boat.at_sea to be false
    #     try:
    #         boat.at_sea = False;
    #         boat.put();
    #     except:
    #         self.response.write(json.dumps({"error": "Error docking boat."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 500;
    #         return
    #
    #     # Send response
    #     self.response.status_int = 204;
    #
    #
    # def delete(self, boat_id, slip_id):
    #     print("DockingHandler: DELETE: Boat to Sea");
    #
    #     # Get & Verify Departure Date from Query String
    #     try:
    #         dep_date_param = self.request.GET["departure"];
    #         datestring = str(dep_date_param);
    #         departure_date = datetime.strptime(datestring, "%m/%d/%Y").date();
    #     except:
    #         self.response.write(json.dumps({"error": "Invalid `departure` parameter"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Convert boat_id and slip_id to ndb objects
    #     try:
    #         boat_key = ndb.Key(urlsafe=boat_id);
    #         boat = boat_key.get()
    #         boatURL = boatsURL + "/" + boat_id;
    #         if (boat == None):
    #             raise TypeError
    #     except:
    #         self.response.write(json.dumps({"error": "Invalid inputs"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     try:
    #         slip_key = ndb.Key(urlsafe=slip_id);
    #         slip = slip_key.get()
    #         if (slip == None):
    #             raise TypeError
    #     except:
    #         self.response.write(json.dumps({"error": "Invalid inputs"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Verify Boat Not At Sea, reject if not
    #     if (boat.at_sea == True):
    #         self.response.write(json.dumps({"error": "Boat already at sea"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Verify Slip is NOT Empty, reject if not
    #     if (slip.current_boat == None) and (slip.current_boat_url == None) and (slip.arrival_date == None):
    #         self.response.write(json.dumps({"error": "Slip already empty"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #         #### Cases not tested: when any of the three clauses are None...
    #
    #     # Update Boat to At Sea
    #     try:
    #         boat.at_sea = True;
    #         boat.put()
    #     except:
    #         # print("Cannot update boat");
    #         self.response.write(json.dumps({"error": "Cannot update boat"}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Update Slip
    #     try:
    #         # Remove current_boat data (boat, url, and arrival date)
    #         slip.arrival_date = None;
    #         slip.current_boat = None;
    #         slip.current_boat_url = None;
    #         slip.departure_history.append({
    #             "departure_date": departure_date,
    #             "departed_boat": boat_id
    #         })
    #         slip.put()
    #         #print("UPDATED SLIP", slip)
    #     except:
    #         #print("Cannot update slip");
    #         # Undo boat update
    #         boat.at_sea = False;
    #         boat.put()
    #
    #         # Send Response
    #         self.response.write(json.dumps({"error": "Cannot update slip."}));
    #         self.response.headers.add('Content-Type', "application/json");
    #         self.response.status_int = 400;
    #         return
    #
    #     # Send response
    #     self.response.status_int = 204;