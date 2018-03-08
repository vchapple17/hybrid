from google.appengine.ext import ndb
from datetime import datetime
import json

class DeviceList(ndb.Model):
    device_key = ndb.StringProperty()
    start_datetime = ndb.DateProperty()
    end_datetime = ndb.DateProperty()
