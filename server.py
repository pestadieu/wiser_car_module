#!/usr/bin/python3

# Comment se connecter à la wifi: https://gist.github.com/taylor224/516de7dd0b707bc0b1b3
import time
import sys
import socket
import queue
import wifi
import json
from threading import Thread
from pprint import pprint

class server(Thread):
	
	#json_file = json.loads('car.json')
	
	def __init__(self, queue_server_obd, queue_obd_server):
		Thread.__init__(self)
		self.name = "server"
		self.queue_server_obd = queue_server_obd
		self.queue_obd_server = queue_obd_server
	
	def run(self):
		while (true):
			print "Starting TCP client on" 
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#sock.connect(http://localhost/wiser/cars,80)
			#sock.connect(http://localhost:8082/wiser/rsu/123/cars)
			#sock.connect(http://loacalhost/wosers/cars/stop,80)
			t = time.time()
			while (time.time() - t <= 1.0):
			received = sock.recv(1024) 
			#print "Jte demande la vitesse maggle"
			sleep(1)
			#queue_server_obd.put(0D)
			print "Je reçois la vitesse maggle"
			queue_obd_server.get(0D)
			# send signal stop to vehicle
			if (json_file[action][stop]== True):
				queue_server_obd.put("EE")		
		
	def listen(self, interface):
		print "Envoie la demannde"
		
	
		

    
    
    

















		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
	
	
