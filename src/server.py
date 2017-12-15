#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import simplejson
import RPi.GPIO as GPIO
import time

ADDR = 'localhost'
PATH = '/wiser/cars/stop'
PORT = 8081
QUEUE = "queue_server_obd"

class handle_led(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.name = "led"

	def run(self):
                t = time.time()
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18,GPIO.OUT)
                while((time.time() - t) < 10.0):
                        print("blink !!")
                        GPIO.output(18, GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(18, GPIO.LOW)
                        time.sleep(1)
                GPIO.cleanup()
                return

class Serv(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		return	

	def do_POST(self):
		print("Got post!!")
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		self.send_response(200)
		self.end_headers()
		data = simplejson.loads(self.data_string)
		if(data["action"]["stop"] == "true"):
			 #QUEUE.put("EE")
			 thread_led = handle_led()
			 thread_led.start()
			 print("Stop the car !!!!!!")
		self._set_headers()
		return

class server(Thread):

	def __init__(self, queue_server_obd, queue_obd_server):
		Thread.__init__(self)
		self.name = "server"
		QUEUE = queue_server_obd
		self.queue_server_obd = queue_server_obd
		self.queue_obd_server = queue_obd_server

	def run(server_class=HTTPServer, handler_class=Serv, port=PORT):
		server_address = (ADDR, port)
		httpd = HTTPServer(server_address, handler_class)
		print('Starting httpd...')
		httpd.serve_forever()


if( __name__=="__main__" ):
        server_address = (ADDR, PORT)
        httpd = HTTPServer(server_address, Serv)
        print('Starting httpd...')
        httpd.serve_forever()

