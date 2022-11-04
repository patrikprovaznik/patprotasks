# Flask API
In this project we developed small application using Flask framework.
___
### What is Flask?
Flask is a web framework that provides libraries to build lightweight web applications in python.  
If u want to learn more about Flask framework and try to create some simple Hello World! Flask app by yourself please
visit this [website](https://www.educative.io/answers/how-to-create-a-hello-world-app-using-python-flask).
___
## Requirements
Python 3.10 +, Postman API (or other similar tool)
___
## How to run Flask app (server side)
* Step 1: Make sure you have Python.
* Step 2: Clone this repository:
  ```commandline
  git clone https://github.com/patrikprovaznik/patprotasks
  ```
* Step 3: Install the requirements: 
  ```commandline
  pip install -r requirements.txt
  ```
* Step 4: Go to this app's directory and start server by running:
  ```commandline
  python3 interface_api.py
  ```
* Step 5: To see your application we recommend to use Postman API.
___
## How to use Flask app
In your Postman app create 4 endpoints at these specific URLS:
***
### Users endpoint
***
1. GET <http://127.0.0.1:5000/get-all-interfaces> - to get all interfaces from server.  
RESPONSE will be view of all interfaces in json format, e.g. :
```json
[
    {
        "cisco-ethernet:ethernet": {},
        "cisco-pw:pw-neighbor": {
            "load-balance": {}
        },
        "enabled": true,
        "ietf-ip:ipv4": {},
        "ietf-ip:ipv6": {
            "address": [
                {
                    "ip": "2000:500:5::1",
                    "prefix-length": 48
                }
            ],
            "ietf-ipv6-unicast-routing:ipv6-router-advertisements": {}
        },
        "link-up-down-trap-enable": "enabled",
        "name": "FastEthernet0/0/1",
        "type": "ianaift:ethernetCsmacd"
    },
    ...
]
```
2. GET <http://127.0.0.1:5000/get-interface/name_of_interface> - to get single interface based on desired name from server.  
RESPONSE:
```json
    {
        "name": "FastEthernet0/0/0",
        "description": "FE000",
        "type": "ianaift:ethernetCsmacd",
        "enabled": false,
        "link-up-down-trap-enable": "enabled",
        "cisco-ethernet:ethernet": {},
        "cisco-pw:pw-neighbor": {
          "load-balance": {}
        },
        "ietf-ip:ipv4": {},
        "ietf-ip:ipv6": {
          "ietf-ipv6-unicast-routing:ipv6-router-advertisements": {}
        }
      }
```
3. POST <http://127.0.0.1:5000/get-interfaces> - to return several interfaces in based on the json input from server. 
REQUEST:
```json
      {
       "input": {
           "interfaces": [{
               "name": "FastEthernet0/0/1",
               "type": "ianaift:ethernetCsmacd"
           },
           {
               "name": null,
               "type": "ianaift:ethernetCsmacd",
               "enabled": false
           }]
       }
}
```
RESPONSE will be view of several interfaces in json format based on the json input, e.g. :
```json
[
    {
        "cisco-ethernet:ethernet": {},
        "cisco-pw:pw-neighbor": {
            "load-balance": {}
        },
        "enabled": true,
        "ietf-ip:ipv4": {},
        "ietf-ip:ipv6": {
            "address": [
                {
                    "ip": "2000:500:5::1",
                    "prefix-length": 48
                }
            ],
            "ietf-ipv6-unicast-routing:ipv6-router-advertisements": {}
        },
        "link-up-down-trap-enable": "enabled",
        "name": "FastEthernet0/0/1",
        "type": "ianaift:ethernetCsmacd"
    },
    ...
]
```
4. DELETE <http://127.0.0.1:5000/delete-interface/name_of_interface> - to delete one of the interfaces from server.  
RESPONSE will be view of deleted/not deleted desired interface with message (if delete was successful or not) in json 
format, e.g. :
```json
{
    "FastEthernet0/0/0": {
        "info": "DELETE WAS SUCCESSFUL"
    }
}
```
---
## How to run client app (client side)
