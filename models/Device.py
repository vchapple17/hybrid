from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from Color import Color, getColorStringFromEnum, getColorEnumFromString
from DeviceModel import DeviceModel, getDeviceModelStringFromEnum, getDeviceModelEnumFromString

from datetime import datetime
import json

class Device(ndb.Model):
    color = msgprop.EnumProperty(Color, required=True)
    model = msgprop.EnumProperty(DeviceModel, required=True)
    is_rented = ndb.BooleanProperty(default=False, required=True)
    serial_no = ndb.StringProperty(required=True)

    def serializeDevice(self, pre_url):
        if (type(pre_url) != type("")):
            return None
        ret = {
            "url": str(pre_url + "/" + self.key.urlsafe()),
            "id": self.key.urlsafe(),
            "color": getColorStringFromEnum(self.color),
            "model": getDeviceModelStringFromEnum(self.model),
            "serial_no": self.serial_no,
            "is_rented": self.is_rented
        }
        return json.dumps(ret);

    @classmethod
    def validateDevicePostRequest(self, obj):
        try:
            for key in obj:
                # Check that key is a valid input ONLY
                if (key == "color"):
                    color = obj["color"];
                elif (key == "model"):
                    model = obj["model"];
                elif (key == "serial_no"):
                    serial_no = obj["serial_no"];
                else:
                    # Invalid Information Given in json
                    raise TypeError

            # Ensure each variable was set
            if (color == None ):
                raise TypeError
            if (model == None ):
                raise TypeError
            if (serial_no == None ):
                raise TypeError

            # Check Enum String is valid enum
            if (getDeviceModelEnumFromString(model) == None):
                raise TypeError

            # Check Enum String is valid enum
            if (getColorEnumFromString(color) == None):
                raise TypeError

            return True
        except(TypeError):
            # Too many attributes OR too few attributes
            return False
        except:
            print("error getColorEnumFromString")
            return False

    @classmethod
    def validateDevicePatchRequest(self, obj):
        if (obj == {}):
            return False
        try:
            # Reject extra keys
            color = None
            model = None
            serial_no = None

            for key in obj.keys():
                # Check that key is a valid input ONLY
                if (key == "color"):
                    color = obj["color"];
                elif (key == "model"):
                    model = obj["model"];
                elif (key == "serial_no"):
                    serial_no = obj["serial_no"];
                else:
                    # Invalid Information Given in json
                    raise TypeError

            # Ensure at least one variable was set
            if (color == None ) and (model == None ) and (serial_no == None ):
                raise TypeError

            # Check Group Enum String is valid enum
            if ( color != None ):
                if (getColorEnumFromString(color) == None):
                    raise TypeError

            # Check Group Enum String is valid enum
            if ( model != None ):
                if (getDeviceModelEnumFromString(model) == None):
                    raise TypeError

            # Passed all tests, so valid
            return True

        except(TypeError):
            # Too many attributes or too few attributes
            return False
        except:
            print("Error: validateDevicePatchRequest")
            return False

    def canDelete(self):
        if (self.is_rented == False):
            return True
        return False
