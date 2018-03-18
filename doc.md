**Inventory API**    Valerie Chapple

## Device Example JSON

| Name | Type | Description |
|--------|----------|---------|
| `url` | `string` | **Required.** URL with auto-generated unique id |
| `id` | `string` | **Required.** Auto-generated unique id |
| `color` | `string` | **Required.** Color Enum of device |
| `model` | `string` | **Required.** Model Enum of device |
| `serial_no` | `string` | **Required.** Serial Number of device|
| `is_rented` | `boolean` | **Required.** Default is `false`|

```
{
  "url": "https://.../devices/kj0987a234bcdasdf12",
  "id":"kj0987a234bcdasdf12",        
  "color": "SPACE_GRAY",  
  "model":"LENOVO",   
  "serial_no":"ASDFASDF123",          
  "is_rented":false        
}
```

**Valid Colors**: `SILVER`, `SPACE_GRAY`, `GOLD`, `ROSE_GOLD`

**Valid Models**: `LENOVO`, `IPAD_4TH`, `IPAD_AIR`, `IPAD_AIR2`

## User Example JSON

| Name | Type | Description |
|--------|----------|---------|
| `url` | `string` | **Required.** URL with auto-generated unique id |
| `id` | `string` | **Required.** Auto-generated unique id |
| `first_name` | `string` | **Required.** User first name|
| `family_name` | `string` | **Required.** User family/last name|
| `group` | `string` | **Required.** Group Enum|
| `device_id` | `string` | ID of the current device, null if empty |
| `start_date` | `string` | Datetime that current device rented in "DD/MM/YYYY HH:MM", null if empty  |


```
{
  "url": "https://.../users/123abc",
  "id":"123abc",              
  "first_name": "Val",   
  "family_name": "Chapple",                
  "group": "CLASS_2018",
  "device_id":"kj0987a234bcdasdf12",    
  "start_date":"1/1/2015 18:23",  
}
```
**Valid Groups**: `STAFF`, `CLASS_2018`, `CLASS_2019`, `CLASS_2020`, `CLASS_2021`

## View a list of devices

Returns an array of device information in JSON, including urls to each device.

```
GET /devices
```

**Response**

```
Status: 200 OK

[
  {
    "url": "https://.../devices/kj0987a234bcdasdf12",
    "id":"kj0987a234bcdasdf12",        
    "color": "SPACE_GRAY",  
    "model":"LENOVO",   
    "serial_no":"ASDFASDF123",          
    "is_rented":false        
  }
]
```

## View a single device

Returns information of a device with `{device_id}` in JSON, including the url to the device.

```
GET /devices/{device_id}
```

**Response**
```
Status: 200 OK

{
  "url": "https://.../devices/kj0987a234bcdasdf12",
  "id":"kj0987a234bcdasdf12",        
  "color": "SPACE_GRAY",  
  "model":"LENOVO",   
  "serial_no":"ASDFASDF123",          
  "is_rented":false        
}
```

## View a list of users

Returns an array of user information in JSON, including urls to each user.

```
GET /users
```

**Response**

```
Status: 200 OK

[
  {
    "url": "https://.../users/123abc",
    "id":"123abc",              
    "first_name": "Val",   
    "family_name": "Chapple",                
    "group": "CLASS_2018",
    "device_id":"kj0987a234bcdasdf12",    
    "start_date":"1/1/2015 18:23",  
  }
]
```

## View a single user

Returns information of a user with `{user_id}` in JSON, including the url to the user.

```
GET /users/{user_id}
```

**Response**
```
Status: 200 OK

{
  "url": "https://.../users/123abc",
  "id":"123abc",              
  "first_name": "Val",   
  "family_name": "Chapple",                
  "group": "CLASS_2018",
  "device_id":"kj0987a234bcdasdf12",    
  "start_date":"1/1/2015 18:23",  
}
```


## Create a new device

```
POST /devices
```
**Input**

| Name | Type | Description |
|--------|----------|---------|
| `color` | `string` | **Required.** Color Enum of device |
| `model` | `string` | **Required.** Model Enum of device
| `serial_no` | `string` | **Required.** Serial Number of device|

Invalid data, extra data, or incorrect data types will be rejected.

**Note**: A new device defaults to `false` for `is_rented`, and the device `id` is auto-generated on the server.

**Request Body**

```
{
  "color": "SPACE_GRAY",
  "model": "LENOVO",
  "serial_no": "ASDF1234567"
}
```

**Response**
```
Status: 201 Created

{
  "url": "https://.../devices/dasdf1234hl",
  "id": "dasdf1234hl",
  "color": "SPACE_GRAY",
  "model": "LENOVO",
  "serial_no": "ASDF1234567",
  "is_rented": false
}
```

## Create a new user

```
POST /users
```
**Input**

| Name | Type | Description |
|--------|----------|---------|
| `first_name` | `string` | **Required.** User first name|
| `family_name` | `string` | **Required.** User family name|
| `group` | `string` | **Required.** Group Enum|

Invalid data, extra data, or incorrect data types will be rejected.

**Note 1**: A new user defaults to no devices checked out. That is, `device_id` and `start_date` default to `null`.

**Note 2**: The user `id` is auto-generated on the server.

**Request Body**

```
{
  "first_name": "Larry",
  "family_name": "Chapple",
  "group": "STAFF",
}
```

**Response**
```
Status: 201 Created

{
  "url": "https://.../users/456abc",
  "id":"456abc",
  "first_name": "Larry",
  "family_name": "Chapple",
  "group": "STAFF",
  "device_id": null,
  "start_date": null
}
```

## Edit a device

```
PATCH /devices/{device_id}
```
**Input**

| Name | Type | Description |
|--------|----------|---------|
| `color` | `string` | Color Enum of device |
| `model` | `string` | Model Enum of device
| `serial_no` | `string` | Serial Number of device|

Invalid data, extra data, or incorrect data types will be rejected.

**Note**: The property `is_rented` can only be changed by checking the device out or in.

**Request Body**

```
{
  "color": "GOLD",
}
```

**Response**
```
Status: 200 OK

{
  "url": "https://.../devices/dasdf1234hl",
  "id": "dasdf1234hl",
  "color": "GOLD",
  "model": "LENOVO",
  "serial_no": "ASDF1234567",
  "is_rented": true
}
```



## Edit a user

```
PATCH /users/{user_id}
```
**Input**

| Name | Type | Description |
|--------|----------|---------|
| `first_name` | `string` | User first name|
| `family_name` | `string` | User family name|
| `group` | `string` | Group Enum|

Invalid data, extra data, or incorrect data types will be rejected.

**Note**: All other user properties can only be changed by checking a device in or out.

**Request Body**

```
{
  "group": "STAFF"
}
```

**Response**
```
Status: 200 OK

{
  "url": "https://.../users/456abcd",
  "id": "456abcd",
  "first_name": "Sharon",
  "family_name": "Chapple",
  "group": "STAFF",
  "device_id": null,
  "start_date": null,
}
```


## Delete a device

```
DELETE /devices/{device_id}
```
**Response**
```
Status: 204 No Content
```
Device is removed from data store only if `is_rented` equals `false`.

## Delete a user

```
DELETE /users/{user_id}
```

**Response**
```
Status: 204 No Content
```
User is removed from data store only if `device_id` equals `null` and `start_date` equals `null`.

## Set a Device to a user
```
PUT /devices/{device_id}/users/{user_id}
```

* The user's property of `device_id` is set to that of the device.
* The user's property of  `start_date` are set to the current datetime.
* The device's properties of `is_rented` is set to `false`.
* Request will be rejected if the device is already checked out or the user already has a device.

**Response**
```
Status: 204 No Content
```

## Set a Device to Available

```
DELETE /users/{user_id}/devices/{device_id}
```

* The user's properties of `device_id` and `start_date` are set to `null`.
* The device's property of `is_rented` is set to `false`.
* Request will be rejected if the device is already checked in or the user already doesn't have a device.


**Response**
```
Status: 204 No Content
```
