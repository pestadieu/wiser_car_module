#!/usr/bin/python3

import socket

from threading import Thread

INTERFACE = "vcan0"

class OBD_handler(Thread):
		
	def __init__(self, queue_server_obd, queue_obd_server):
		Thread.__init__(self)
		self.name = "OBD_handler"
		self.queue_server_obd = queue_server_obd
		self.queue_obd_server = queue_obd_server
		
	def run(self):
		
	def send_obd_frame(self, obd_pid):
		s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
		s.bind((INTERFACE,))
		
		
	def receive_obd_frame(self):

	
