#!/usr/bin/python3

# Comment se connecter à la wifi: https://gist.github.com/taylor224/516de7dd0b707bc0b1b3

import socket

from threading import Thread

class server(Thread):
	
	def __init__(self, queue_server_obd, queue_obd_server):
		Thread.__init__(self)
		self.name = "server"
		self.queue_server_obd = queue_server_obd
		self.queue_obd_server = queue_obd_server
		
	def run(self):
      print "Starting TCP server on" 
	
	def listen(self, interface):
	
	
	
