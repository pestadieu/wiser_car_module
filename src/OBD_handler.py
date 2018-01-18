#!/usr/bin/python3
# -*- coding: utf-8 -*-
# WiFi connection: https://gist.github.com/taylor224/516de7dd0b707bc0b1b3

import socket
import struct
import sys
import time
import json
import http.client, urllib
from threading import Thread
from queue import Queue, Empty

ADDR = "localhost"
PORT = "8083"
PATH = "/wiser/rsu"

INTERFACE = "vcan0"
can_frame_fmt = "=IB3x8s"

class OBD_handler(Thread):
		
	def __init__(self, queue_server_obd, queue_obd_server):
		Thread.__init__(self)
		self.name = "OBD_handler"
		self.queue_server_obd = queue_server_obd
		self.queue_obd_server = queue_obd_server
		#self.client = client()
		
	def run(self):
		while(True):
			t = time.time()
			while((time.time() - t) < 1.0):
				try:
					obd_pid = self.queue_server_obd.get(False)
					data = send_recv_obd_frame(obd_pid)
				except Empty:
					pass
			client_send()
			
def send_recv_obd_frame(obd_pid):
	print("send_obd_frame: obd_pid = " + obd_pid)
	s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
	s.bind((INTERFACE,))
	try:
		s.send(build_can_frame(0x7DF, b'\x02\x01\x0d'))
	except socket.error:
		print('Error sending CAN frame')
	data = recieve_can_frame(s)
	return data
	
def build_can_frame(can_id, data):
	can_dlc = len(data)
	data = data.ljust(8, b'\x00')
	a = struct.pack(can_frame_fmt, can_id, can_dlc, data)
	return a

def recieve_can_frame(socket):
	frame, addr = socket.recvfrom(16)
	can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
	return data[3:can_dlc]
	
def process_obd(data, obd_pid):
	if(str(obd_pid) == "0D"):
		return(str(int.from_bytes(data, byteorder='big')))
	elif(str(obd_pid) == "EE"):
		return("OK")
		
def client_send():
	change_speed_in_json(retreive_speed())
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(ADDR+":"+PORT)
	conn.request("POST", PATH, 3, headers)
	response = conn.getresponse()
	print(response.status, response.reason)
	resp = response.read()
    
def retreive_speed():
	speed = send_obd_frame("0D")
	return speed

def retreive_rpm():
	speed = send_obd_frame("0C")
	return speed

def retreive_engine_temp():
	speed = send_obd_frame("05")
	return speed

def retreive_engine_presure():
	speed = send_obd_frame("0A")
	return speed

def change_speed_in_json(speed):
	with open("1.json", "r") as jsonFile:
		data = json.load(jsonFile)

	tmp = data["params"]["speed"]
	data["params"]["speed"] = str(speed)

	with open(JSON_PATH, "w") as jsonFile:
		json.dump(data, jsonFile)
