#!/usr/bin/python3

import socket
import struct
import sys

from threading import Thread

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
			while(True):
				obd_pid = self.queue_server_obd.get() # "0D" -> vitesse, "EE" -> Stop
				if not obd_pid:
					break
			data = send_obd_frame(obd_pid)
			data = process_obd(data, obd_pid)
			self.queue_obd_server.put(data)
		
def send_obd_frame(obd_pid):
	s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
	s.bind((INTERFACE,))
	try:
		s.send(build_can_frame(0x7DF, b'\x02\x01\x0d'))
		#s.send(b'\x07\xdf\x00\x00\x03\x00\x00\x00\x02\x01\x0C\x00\x00\x00\x00\x00')
	except socket.error:
		print('Error sending CAN frame')
	data = receive_can_frame()
	return data
	
def build_can_frame(can_id, data):
	can_dlc = len(data)
	data = data.ljust(8, b'\x00')
	a = struct.pack(can_frame_fmt, can_id, can_dlc, data)
	#print(a)
	return a

def recieve_can_frame():
	frame, addr = s.recvfrom(16)
	can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
	return data[3:can_dlc]
	
def process_obd(data, obd_pid):
	if(str(obd_pid) == "0D"):
		return(str(int.from_bytes(data, byteorder='big')))
	elif(str(obd_pid) == "EE"):
		return("OK")
		
	
	
	
	
	
