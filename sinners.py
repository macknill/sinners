#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json


def log(text):
	print text

try:
	file_stat = open('status.json','r')
except:
	log("No file status.json. Script is close")
	raise SystemExit(1)
status_json = file_stat.read()

try:
	sock = socket.socket()
	sock.bind(('127.0.0.1', 9090))
	sock.listen(1)
	while True:
		#status = json.loads(standart_json)
		log("Wait to connect")
		conn, addr = sock.accept()
		data = conn.recv(1024)
		print data
		print 'connected:', addr

		conn.send(status_json)
		conn.close()	
		log("Connect close")

		
except RuntimeError, KeyboardInterrupt:
	conn.close()
