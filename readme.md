
# api

## Deploy webapp2


## Requirements
* The backend must have at least 1 entity with 4 or more properties
* The backend must also meet at least one of the following requirements
    * User accounts are supported (ie. there is data tied to specific users that only they can see or modify) and they are tied to a 3rd party provider. You could use OAuth to access basic account info or you could use something like OpenIDConnect for authentication. You should not simply handle all account creation and management yourself.
    * There is additional entity with 4 or more properties that is related to the original entity and the items can be added or removed from the relationship (like books being checked out to customers)
* It needs to model different data than the one for the homework
* It must use a non-relational database on a cloud provider (Google App Engine with NDB is recommended)
* It must meet REST requirements of using resource based URLs and representations of things via links
