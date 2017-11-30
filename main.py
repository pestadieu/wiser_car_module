#!/usr/bin/python3

from queue import Queue
# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch12s03.html

from client import *
from OBD_handler import *

if(__name__ == '__main__'):
	queue_client_obd = Queue()
	queue_obd_client = Queue()

	thread1 = client(queue_client_obd, queue_obd_client)
	thread2 = OBD_handler(queue_client_obd, queue_obd_client)
	
	thread1.start()
	thread2.start()
	
	# Killing the threads
	thread1.join()
    thread2.join()
