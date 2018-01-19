#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

JSON_PATH = "src/data/1.json"

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
		if(obd_pid == "0D"):
			s.send(build_can_frame(0x7DF, b'\x02\x01\x0d'))
		elif(obd_pid == "0C"):
			s.send(build_can_frame(0x7DF, b'\x02\x01\x0c'))
		elif(obd_pid == "05"):
			s.send(build_can_frame(0x7DF, b'\x02\x01\x05'))
		elif(obd_pid == "0A"):
			s.send(build_can_frame(0x7DF, b'\x02\x01\x0a'))
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
		
def client_send():
	change_json("speed", retreive_speed())
	change_json("coolant_temp", retreive_engine_temp())
	change_json("rpm", retreive_rpm())
	change_json("fuelPressure", retreive_fuel_pressure())
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(ADDR+":"+PORT)
	conn.request("POST", PATH, 3, headers)
	response = conn.getresponse()
	print(response.status, response.reason)
	resp = response.read()
    
def retreive_speed():
	speed = send_recv_obd_frame("0D")
	return str(int.from_bytes(speed, byteorder='big'))

def retreive_rpm():
	rpm = send_recv_obd_frame("0C")
	return str(int.from_bytes(rpm, byteorder='big'))

def retreive_engine_temp():
	engine_temp = send_recv_obd_frame("05")
	return str(int.from_bytes(engine_temp, byteorder='big'))

def retreive_fuel_pressure():
	fuel_pressure = send_recv_obd_frame("0A")
	return str(3*int.from_bytes(fuel_pressure, byteorder='big'))

def change_json(field, value):
	with open(JSON_PATH, "r") as jsonFile:
		data = json.load(jsonFile)

	data["params"][field] = value

	with open(JSON_PATH, "w") as jsonFile:
		json.dump(data, jsonFile)
