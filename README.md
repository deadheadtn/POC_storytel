# Basic REST-API for Messaging


**Requirements**

 - python3.7 and higher
 - updated version of pip
 - redis-server


### Installation

Docker will be installed using this script
$    `./setup.sh`

## Build and Run the App With Docker
Run `docker-compose build` to build the containers.  
Run `docker-compose up` to start the app.  
Run `docker-compose up -d` to start the app in detached mode.  
Run `docker-compose down` to stop the app.

## API Endpoints


### Create (Message)
```
POST /api/message
```
```
PUT /api/message
```

**Parameters:**

Name | Type | Mandatory | Description | Format
------------ | ------------ | ------------ | ------------ | ------------
Message | STRING | YES | This parameter is very important | JSON

**Data Source:**
in-memory storage be careful

**Response:**
```javascript
{
  "url": "{host}/api/message/{id}"
}
```
------
### Display (Message)
```
GET /api/message/{id}
```

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
 None| None  |None  |

**Data Source:**
in-memory storage be careful

**Response:**
```javascript
[Message_here]
```
