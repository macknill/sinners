#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import threading
import time
import socket_to_web

def log(text):
	print text

try:
	file_stat = open('status.json','r')
	file_cmd = open('cmd.json','r')
except:
	log("No files json. Script is close")
	raise SystemExit(1)

try:
	status_json = file_stat.read()
	cmd_json = file_cmd.read()
except:
	log("Read files json error. Script is close")
	raise SystemExit(1)

try:
	status = json.loads(status_json)
	cmd = json.loads(cmd_json)
except:
	log("Error decode json files. Script is close")
	raise SystemExit(1)


web = socket_to_web.LinkToWeb(status, cmd)
try:
	
	t1 = threading.Thread(target = web.start)	
	log("Socket Threading start")
	t1.start()
	while True:
		time.sleep(1)	
except:
	web.stop()




