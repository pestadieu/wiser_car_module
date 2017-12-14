#!/usr/bin/python3
# -*- coding: utf-8 -*-

from queue import Queue

from server import *
from OBD_handler import *

if(__name__ == '__main__'):
	queue_server_obd = Queue()
	queue_obd_server = Queue()

	thread1 = OBD_handler(queue_server_obd, queue_obd_server)   # OBD handler
	thread2 = server(queue_server_obd, queue_obd_server)        # Server
	
	thread1.start()
	thread2.start()
