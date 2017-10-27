#!/usr/bin/python3

from queue import Queue
# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch12s03.html

from server import *
from OBD_handler import *

if(__name__ == '__main__'):
	queue_server_obd = Queue()
	queue_obd_server = Queue()

	thread1 = server(queue_server_obd, queue_obd_server)
	thread2 = OBD_handler(queue_server_obd, queue_obd_server)
	
	thread1.start()
	thread2.start()
