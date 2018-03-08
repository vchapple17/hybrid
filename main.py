#!/usr/bin/env python
import sys
sys.path.append("./models/")
sys.path.append("./control/")

import webapp2
from webapp2 import Route
from UserHandler import UsersHandler#, UserHandler, RentingHandler
# from device_handler import DevicesHandler, DeviceHandler
from webapp2_extras.routes import RedirectRoute, PathPrefixRoute

DEBUG_FLAG = True


# Monkey Patch for webapp2 PATCH
#https://stackoverflow.com/questions/16280496/patch-method-handler-on-google-appengine-webapp2

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods


application = webapp2.WSGIApplication([

    Route('/users', handler=UsersHandler, name='users'),
    # PathPrefixRoute( '/users',[
    #     Route('/', handler=UsersHandler, name='users'),
    #     Route('/<user_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=UserHandler, name='user'),

        # Route('/<user_id:([A-Z]|[a-z]|[0-9]|[-._])+>/users/<device_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=RentingHandler, name='renting'),

    # ]),

    # Route('/devices', handler=DevicesHandler, name='devices'),
    # PathPrefixRoute( '/devices',[
    #     Route('/', handler=DevicesHandler, name='devices'),
    #     Route('/<device_id:([A-Z]|[a-z]|[0-9]|[-._])+(/)?>', handler=DeviceHandler, name='device'),
    # ]),

], debug=DEBUG_FLAG)
