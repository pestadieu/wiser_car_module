#!/usr/bin/python3

import requests
import json
import socket
import sys
from pprint import pprint

DOMAIN_NAME = "localhost"
MSG_MAX_LEN = 4096

# Receive speed
addr = "http://" + DOMAIN_NAME + "/wiser/cars"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(addr, 80)
while True:
    connection, client_address = sock.accept()
    data = sock.recvmsg(MSG_MAX_LEN)
    pprint(data)
    print("La vitesse est " + data["params"["speed"]] + "km/h")
    
    
# Send stop request
with open('1.json') as data_file:    
    json = json.load(data_file)
    
addr = "http://" + DOMAIN_NAME + "/wiser/cars/stop"
r = requests.post(addr, data=json)

