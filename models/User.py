from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

# from DeviceList import DeviceList
from Group import Group, getGroupEnumFromString
from datetime import datetime
import json

class User(ndb.Model):
    first_name = ndb.StringProperty()
    family_name = ndb.StringProperty()
    group = msgprop.EnumProperty(Group)
    device_id = ndb.StringProperty()
    start_datetime = ndb.DateTimeProperty()

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
        return json.dumps(ret);

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
