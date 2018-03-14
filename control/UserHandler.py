#!/usr/bin/env python
import sys
sys.path.append("./models/")

from webapp2 import RequestHandler
import webapp2_extras
import json
from google.appengine.ext import ndb
from datetime import datetime
from const import baseURL, usersURL
from User import User
from Group import getGroupEnumFromString

class UsersHandler(RequestHandler):
    def get(self):
        print("UsersHandler: GET LIST")
        # Retrieve boats
        users = User.query().fetch()

        # Send response
        res = []
        for user in users:
            obj = user.serializeUser( usersURL );
            res.append(obj)
        # self.response.content_type = 'text/plain'
        self.response.headers.add('Content-Type', "application/json")
        self.response.status_int = 200;
        self.response.out.write(json.dumps(res))
        return

    def post(self):
        print("UsersHandler: CREATE POST")
        # Save Request Body
        try:
            req = self.request.body
            obj = json.loads(req)

            if (User.validateUserPostRequest( obj )):
                group_enum = getGroupEnumFromString(obj["group"])
                # User req contains exactly what is required
                user = User( first_name=obj["first_name"], family_name=obj["family_name"], group=group_enum)
                user.put()
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
            self.response.write( json.dumps(user.serializeUser(usersURL)) )
        except:
            self.response.write(json.dumps({"error": "Cannot write response."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 500;
            return

# User identified by id
class UserHandler(RequestHandler):
    def get(self, user_id):
        print("UserHandler: GET 1: " + user_id)
        # Convert boat_id to ndb object
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

        # Send response
        res = user.serializeUser( usersURL );
        # userURL = usersURL + "/" + user_id;
        self.response.content_type = 'application/json'
        self.response.status_int = 200;
        self.response.write(json.dumps(res))

    def patch(self, user_id):
        print("UserHandler: PATCH")

        try:
            # Convert boat_id to ndb object
            user_key = ndb.Key(urlsafe=user_id);
            user = user_key.get()
            if (user == None):
                print("UserHandler: User is of type None")
                raise TypeError("User is of type None")
        except:
            self.response.write(json.dumps({"error": "Invalid User ID"}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 404;
            return;
        # Get json from Request Body
        try:
            req = self.request.body;
            obj = json.loads(req);
            print(obj)
            if (User.validateUserPatchRequest( obj )):
                # User req contains exactly what is required
                # Submit Patch
                if (obj["first_name"] != None):
                    user.first_name = obj["first_name"]
                if (obj["family_name"] != None):
                    user.family_name = obj["family_name"]
                if (obj["group"] != None):
                    user.group = getGroupEnumFromString(obj["group"])
                user.put()
            else:
                print("UserHandler: invalid")
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
            self.response.write( json.dumps(user.serializeUser(usersURL)))
            return
        except:
            self.response.write(json.dumps({"error": "Cannot write response."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 500;
            return

    def delete(self, user_id):
        print("UserHandler: DELETE 1")

        # Convert user_id to ndb KEY
        try:
            user_key = ndb.Key(urlsafe=user_id);
            user = user_key.get()
            if (user == None):
                raise TypeError
        except:
            self.response.status_int = 204;
            return


        if (user.canDelete() == False):
            self.response.status_int = 400
            return

        # Delete entity
        try:
            user_key.delete();
        except:
            self.response.write(json.dumps({"error": "Cannot delete entity."}));
            self.response.headers.add('Content-Type', "application/json");
            self.response.status_int = 400;
            return

        # # Send response that boat is deleted
        self.response.status_int = 204;
        self.response.content_type = None;
        return;
