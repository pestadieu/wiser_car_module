#!/usr/bin/python3
# -*- coding: utf-8 -*-

# WiFi connection: https://gist.github.com/taylor224/516de7dd0b707bc0b1b3
import sys
import socket
import json
from threading import Thread
import http.client, urllib

#from OBD_handler import *

ADDR = "localhost"
PORT = "8083"
PATH = "/wiser/rsu"
JSON_PATH = "./data/1.json"

def client_send():
	change_speed_in_json(retreive_speed())
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(ADDR+":"+PORT)
	conn.request("POST", PATH, json.dumps(self.data), headers)
	response = conn.getresponse()
	print(response.status, response.reason)
	resp = response.read()
    
def retreive_speed():
	speed = send_obd_frame("OD")
	return speed

def change_speed_in_json(speed):
	with open("1.json", "r") as jsonFile:
		data = json.load(jsonFile)

	tmp = data["params"]["speed"]
	data["params"]["speed"] = str(speed)

	with open("1.json", "w") as jsonFile:
		json.dump(data, jsonFile)
