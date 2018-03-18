# Inventory API

# Setup

## Local

Install and set up Google Cloud SDK locally [https://cloud.google.com/sdk/downloads].

## Google Cloud

After you create your project and register it through Google, you can easily upload files and deploy apps using the Google Cloud Shell.[https://console.cloud.google.com/home/dashboard]

# Deployment
To deploy your app for testing and development:

```
dev_appserver.py app.yaml
```

To deploy the app for testing and development with a clean datastore:

```
dev_appserver.py --clear_datastore=yes app.yaml
```

To deploy the app to a server using Google Cloud Shell:
```
gcloud app deploy app.yaml
```

# Documentation

See Documentation: [https://github.com/vchapple17/hybrid/blob/master/doc.md]

# Endpoints

## User

```
GET /users/
POST /users/

GET /users/{user_id}
PATCH /users/{user_id}
DELETE /users/{user_id}
```

## Device

```
GET /devices/
POST /devices/

GET /devices/{slip_id}
PATCH /devices/{slip_id}
DELETE /devices/{slip_id}
```

## Check Out and Check In Device

```
PUT /users/{user_id}/devices/{device_id}
DELETE /users/{user_id}/devices/{device_id}
```
