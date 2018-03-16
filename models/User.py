from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from Device import Device
from Group import Group, getGroupEnumFromString
from datetime import datetime
import json

class User(ndb.Model):
    first_name = ndb.StringProperty()
    family_name = ndb.StringProperty()
    group = msgprop.EnumProperty(Group)
    device_id = ndb.StringProperty(default=None)
    start_datetime = ndb.DateTimeProperty(default=None)

    def serializeUser(self, pre_url):
        if (type(pre_url) != type("")):
            return None
        ret = {
                "url": str(pre_url + "/" + self.key.urlsafe()),
                "id": self.key.urlsafe(),
                "first_name": self.first_name,
                "family_name": self.family_name,
                "group": str(self.group),
                "device_id": self.device_id,
            }
        if self.start_datetime != None:
            ret["start_datetime"] = datetime.strftime(self.start_datetime, "%m/%d/%y %H:%M");
        else:
            ret["start_datetime"] = None
        return ret;

    def checkOutDevice(self, device_id, start_datetime):
        if (type(device_id) != type("")):
            return None
        if (type(start_datetime) != type(datetime.now())):
            return None

        # Check user does not already have a device
        if (self.device_id != None) and (self.device_id != device_id):
            return None

        # Verify Device Exists and is available
        try:
            device_key = ndb.Key(urlsafe=device_id);
            device = device_key.get()
            if (device == None):
                raise TypeError
            if (device.is_rented == True) and (self.device_id  != device_id):
                raise TypeError
        except(TypeError):
            # device does not exist or is unavailable
            return None
        except:
            print("Error checkOutDevice")
            return None

        try:
            # Device Exists and is available
            device.is_rented = True
            device.put()
        except:
            # Error updating device
            return None

        try:
            self.device_id = device_id
            self.start_datetime = start_datetime
            self.put()
        except:
            # Error updating device
            return None

        return True

    def checkInDevice(self, device_id):
        if (type(device_id) != type("")):
            return None

        # Check user has this device
        if (self.device_id != str(device_id)):
            return None

        # Verify Device Exists and is resent
        try:
            device_key = ndb.Key(urlsafe=device_id);
            device = device_key.get()
            if (device == None):
                raise TypeError
            if (device.is_rented == False):
                raise TypeError
        except(TypeError):
            # device does not exist or is not checked out
            return None
        except:
            print("Error checkOutDevice")
            return None

        try:
            # Device Exists and is available
            device.is_rented = False
            device.put()
        except:
            # Error updating device
            return None

        try:
            self.device_id = None
            self.start_datetime = None
        except:
            # Error updating device
            return None

        return True

    def canDelete(self):
        if (self.device_id == None) and (self.start_datetime == None):
            return True
        return False

    @classmethod
    def validateUserPostRequest(self, obj):
        try:
            for key in obj:
                # Check that key is a valid input ONLY
                if (key == "first_name"):
                    first_name = obj["first_name"];
                elif (key == "family_name"):
                    family_name = obj["family_name"];
                elif (key == "group"):
                    group = obj["group"];
                else:
                    # Invalid Information Given in json
                    raise TypeError

            # Ensure each variable was set
            if (first_name == None ):
                raise TypeError
            if (family_name == None ):
                raise TypeError
            if (group == None ):
                raise TypeError

            # Check Group Enum String is valid enum
            if (getGroupEnumFromString(group) == None):
                raise TypeError

            return True
        except:
            # Too many attributes OR too few attributes
            return False

    @classmethod
    def validateUserPatchRequest(self, obj):
        if (obj == {}):
            return False
        try:
            # Reject extra keys
            first_name = None
            family_name = None
            group = None

            for key in obj.keys():
                # Check that key is a valid input ONLY
                if (key == "first_name"):
                    first_name = obj["first_name"];
                elif (key == "family_name"):
                    family_name = obj["family_name"];
                elif (key == "group"):
                    group = obj["group"];
                else:
                    # Invalid Information Given in json
                    raise TypeError

            # Ensure at least one variable was set
            if (first_name == None ) and (family_name == None ) and (group == None ):
                raise TypeError

            # Check Group Enum String is valid enum
            if ( group != None ):
                if (getGroupEnumFromString(group) == None):
                    raise TypeError

            # Passed all tests, so valid
            return True

        except:
            # Too many attributes or too few attributes
            return False
