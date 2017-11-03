#!/usr/bin/python3

# Comment se connecter à la wifi: https://gist.github.com/taylor224/516de7dd0b707bc0b1b3

import sys
import socket
import queue
import wifi
import json
from threading import Thread
from pprint import pprint

class server(Thread):
	
	json_file = json.loads('car.json')
	
	def __init__(self, queue_server_obd, queue_obd_server):
		Thread.__init__(self)
		self.name = "server"
		self.queue_server_obd = queue_server_obd
		self.queue_obd_server = queue_obd_server

		
	def run(self):
		while (true):
			print "Starting TCP server on" 
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			received = sock.recv(1024)
			print "Jte demande la vitesse maggle"
			queue_server_obd.put(0D)
			print "Je reçois la vitesse maggle"
			queue_obd_server.get(0D)
			if (json_file[action][stop]== True):
				queue_server_obd.put("EE")		
		
	def listen(self, interface):
		print "Envoie la demannnde"
		
	# Launching the threads
	queue_server_obd.start()
    queue_obd_server.start()	
		
	# Killing the threads
	queue_server_obd.join()
    queue_obd_server.join()
	
	
	def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)

    return wifilist
    
    def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False
    
    def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False
    
    def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell
    
    return False
    
    
    def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme
    
    
    def Delete(ssid):
    if not ssid:
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        return True

    return False
    
    
    if __name__ == '__main__':
    # Search WiFi and return WiFi list
    print Search()

    # Connect WiFi with password & without password
    print Connect('OpenWiFi')
    print Connect('ClosedWiFi', 'password')

    # Delete WiFi from auto connect list
    print Delete('DeleteWiFi')	
		

    
    
    

















		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
	
	
