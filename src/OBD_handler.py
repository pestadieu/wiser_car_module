#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import struct
import sys
import datetime
import time
import json
import requests
from threading import Thread
from queue import Queue, Empty

ADDR = "192.168.137.6"
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
	d = datetime.datetime.utcnow()
	info = {
		"apiVersion": "1.0",
		"typeOfVehicule": "car",
		"idVehicule": "1234",
		"date": d.isoformat("T") + "Z",
		"params": {
			"speed": retreive_speed(),
			"coolant_temp": retreive_engine_coolant_temp(),
			"rpm": retreive_rpm(),
			"fuelPressure": retreive_fuel_pressure()
			}
		}
	# ~ info = {
		# ~ "apiVersion": "1.0",
		# ~ "typeOfVehicule": "car",
		# ~ "idVehicule": "1234",
		# ~ "date": d.isoformat("T") + "Z",
		# ~ "params": {
			# ~ "speed": "45",
			# ~ "coolant_temp": "30",
			# ~ "rpm": "300",
			# ~ "fuelPressure": "50"
			# ~ }
		# ~ }
	print(info)
	requests.post("http://"+ADDR+":"+PORT+PATH, json=info)
    
def retreive_speed():
	speed = send_recv_obd_frame("0D")
	speed = str(int.from_bytes(speed, byteorder='big'))
	return(speed)

def retreive_rpm():
	rpm = send_recv_obd_frame("0C")
	rpm = str((256 * rpm[0] + rpm[1])/4)
	return(rpm)

def retreive_engine_coolant_temp():
	engine_coolant_temp = send_recv_obd_frame("05")
	print(engine_coolant_temp)
	engine_coolant_temp = str(int.from_bytes(engine_coolant_temp, 'big') - 0x40)
	return(engine_coolant_temp)

def retreive_fuel_pressure():
	fuel_pressure = send_recv_obd_frame("0A")
	fuel_pressure = str(3*int.from_bytes(fuel_pressure, byteorder='big'))
	return(fuel_pressure)

