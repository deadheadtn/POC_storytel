import requests
import json
import base64
import time

def register(user, password):
    url = "http://127.0.0.1:5000/register"
    aDict = {}
    aDict["name"]= user
    aDict["password"]= password
    payload = json.dumps(aDict)
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)

    return(response.json())

def login(user, password):
    url = "http://127.0.0.1:5000/login"
    headers = {'content-type': "application/json"}
    response = requests.get(url, auth=(user, password), headers=headers)
    return(response.json())


def createMessage(message,jwt):
    url = "http://127.0.0.1:5000/api/message"
    aDict = {}
    aDict["Message"]= message
    payload = json.dumps(aDict)
    headers = {
        'x-access-tokens': jwt,
        'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    return(response.json())


def viewMessage(id ,jwt):
    url = "http://127.0.0.1:5000"+id
    headers = {'x-access-tokens': jwt}
    response = requests.get(url, headers=headers)
    return(response.text)


if __name__ == "__main__":
    user = "test"
    password= "test"
    message="teest sadadecret"
    print (register(user, password))
    jwt=login(user, password)['token']
    id=createMessage(message, jwt)['url']
    time.sleep(2)
    print(viewMessage(id,jwt))
