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


### Register (user)
```
POST /register
```

**Parameters:**

Name | Type | Mandatory | Description | Format
------------ | ------------ | ------------ | ------------ | ------------
name | STRING | YES | unique username | JSON
password | STRING | YES | password preferably > 8 characters | JSON

**Data Source:**
in-memory storage be careful

**Response:**
```javascript
{"message":"registered successfully"}
```
------

### Login (user)
```
GET /login
```

**Header:**

Name | value | Mandatory | Description
------------ | ------------ | ------------ | ------------
authorization  | Basic base64(name:pass) | YES |  
content-type | STRING | YES | password preferably > 8 characters

**Data Source:**
in-memory storage be careful

**Response:**
```javascript
{"message":"registered successfully"}
```
------


### Create (Message)
```
POST /api/message
```
```
PUT /api/message
```

**Header:**

Name | value | Mandatory | Description
------------ | ------------ | ------------ | ------------
x-access-tokens | ***JWT from login***| YES | JWT for authentication
content-type | application/json | YES | specifying the content being processed by the API

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

## Security risks/assumptions

### Intro

This REST API serves as a path finder for technical and security assessments providing the requested tasks to perform as follow:
Security Engineer - Coding Challenge

-   A client should be able to **create a message**, and get the URL to the message

-   A client should be able to **view any message**, if the URL is known to the client

-   It should be **infeasible** to guess the URL to a message

-   Messages should only be stored and available on the server for **7 days**, and deleted automatically thereafter.

***I have highlighted the keywords

---
### Message protection
In the view endpoint a **32 characters long alphanumeric** values identifier was used in order to minimise the risk of brute-forcing the id to get access to messages.

Due to time restrictions no authentication or authorisation method was used but confidentiality of information is still preserved.

This system on the other hand have some limitations to what it can handle so I made sure to include how many worker and threads the APP can leverage in order to accomodate a large number of requests and can be modified in the `Dockerfile` an  more specifically in `--workers 1 --threads 8 `


### Advantages of using Redis as in-memory storage
For instance an attacker could supply a set of strings that are known to hash to the same bucket into a hash table in order to turn the O(1) expected time (the average time) to the O(N) worst case, consuming more CPU than expected, and ultimately causing a Denial of Service.
To prevent this specific attack, Redis uses a per-execution pseudo-random seed to the hash function.

Redis implements the SORT command using the qsort algorithm. Currently, the algorithm is not randomized, so it is possible to trigger a quadratic worst-case behavior by carefully selecting the right set of inputs.


### String escaping and NoSQL injection

The Redis protocol has no concept of string escaping, so injection is impossible under normal circumstances using a normal client library. The protocol uses prefixed-length strings and is completely binary safe.
