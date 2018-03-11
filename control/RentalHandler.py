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

class RentingHandler(RequestHandler):
    def put(self, boat_id, slip_id):
        pass
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
    def delete(self, boat_id, slip_id):
        pass
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