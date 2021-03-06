#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from time import gmtime, strftime
from array import array
import re
import shutil
import json
import time

def log(txt):
	print txt

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

def socket_quest(cmd1, status1, rw):
	try:
		sock = socket.socket()
		sock.connect(('127.0.0.1', 9090))
		if rw:
			st_json = json.dumps(cmd1)
			sock.send(st_json)
		else:
			sock.send("none")
		data = sock.recv(1024)
		status2 = json.loads(data)
		for i in range(26):
			status1['rpi'][i] = status2['rpi'][i]
			status1['relay'][i] = status2['relay'][i]
		status1['time'] = status2['time'] 
		status1['arduino'] = status2['arduino'] 
		status1['start'] = status2['start'] 
		sock.close()
		return 1
	except:
		log("No socket server to quest script")
		return 0

socket_connect = 0

class HttpProcessor(BaseHTTPRequestHandler):
	def do_GET(self):
		address = self.path
		self.send_response(200)
		self.send_header('content-type','text/html')
		self.end_headers()
		readwrite = True
		if len(address) > 1:		
			if address.find("start") == 1:	
				log("CMD START")
				cmd["start"] = 1
			elif address.find("reset") == 1:		
				log("CMD RESET")
				cmd["reset"] = 1
			elif address.find("relay_") == 1:	
				log("CMD "+ address)
				find = re.findall('(\d+)', address)
				number = int(find[0]) - 1
				if number < 26:
					cmd["relay"][0] = number
					cmd["relay"][1] = 1	
			elif address.find("favicon.ico"):
				readwtite = False
				try:
					favicon = open('sinners.png','r')
					self.wfile.write(favicon.read())
				except:
					log("No favicon.ico file")
				
			
			self.wfile.write('<script language="JavaScript">window.location.href = "/"</script>')
			socket_quest(cmd, status, readwrite)			
			cmd["start"] = 0
			cmd["reset"] = 0
			cmd["relay"][0] = 0
			cmd["relay"][1] = 0	
  		else:					
			socket_connect = socket_quest(cmd, status, False)				
			self.wfile.write('<!DOCTYPE "html"><html><head><title>Quest Sinners</title><meta http-equiv="Refresh" content="20" />')	
			self.wfile.write("</head><body>")
			self.wfile.write(strftime('%d %b %Y %H:%M:%S', gmtime()))			
			self.wfile.write("</body>")
			self.wfile.write('<form method="get" action="/reset"><button type="submit">Reset Quest</button></form>')			
			if status['start']:
				color = 'green'
			else:
				color = 'red'

			time_temp = "00:00"
			if status['start'] > 0:
				timer = time.localtime(time.time() - status['time'])
				time_temp = time.strftime('%M:%S', timer)

			ReleTable = '<form method="get" action="/start"><button type="submit">Start Quest</button><span style="background:'  + color
			ReleTable += '">  State</span> '+ time_temp +'</form>'
			if status["arduino"]:
				ReleTable +='Arduino: <span style="background: green">Connect</span>'
			else:
				ReleTable += 'Arduino: <span style="background: red">Disconnect</span>'

			if socket_connect:
				ReleTable +='  Socket: <span style="background: green">Connect</span>'
			else:
				ReleTable += '   Socket: <span style="background: red">Disconnect</span>'

			ReleTable += '<TABLE BORDER="1" CELLSPACING="0"><CAPTION>Quest state</CAPTION>'	
			ReleTable += "<TR>";	
			ReleTable += '<TH>#</TH><TH>In/Out</TH><TH>Val</TH><TH>Name</TH>'
			ReleTable += '<TH>#</TH><TH>In/Out</TH><TH>Val</TH><TH>Name</TH>'
			ReleTable += '<TH>#</TH><TH>In/Out</TH><TH>Val</TH><TH>Name</TH>'
			ReleTable += '<TH>#</TH><TH>In/Out</TH><TH>Val</TH><TH>Name</TH>'
			ReleTable += "</TR>"
			RelayString = []
			for i in range(26):	
				if status["relay"][i]:
					color = 'green'
				else:
					color = "red"
				temp = "<TD>"+ str(i+1)+'</TD><TD><form method="get" action="/relay_'+str(i + 1)+'"><button type="submit">Relay '
				temp += str(i + 1) + '</button></form>' + "</TD>"
				temp += '<TD><span style="background: ' + color + '">' + str(status["relay"][i])  + "</span></TD><TD>" + "none" + "</TD>"
				RelayString.append(temp)

			InputString = [];
			for i in range(26):			
				if status["rpi"][i]:
					color = 'green'
				else:
					color = "red"
				temp = "<TD>"+ str(i+1)+'</TD><TD>Input'+str(i+1)+'</TD><TD><span style="background:' + color + '">' + str(status["rpi"][i])
				temp += "</span></TD><TD>" + 'none' + "</TD>"
				InputString.append(temp)
			for i in range(13):
				ReleTable += "<TR>"
				ReleTable += RelayString[i] + RelayString[i + 13] + InputString[i] + InputString[i + 13];
				ReleTable += "</TR>"
		
			ReleTable += "</TABLE>"		
			self.wfile.write(ReleTable)	
			self.wfile.write("</body>")
			self.wfile.write("</html>")
try:
	serv = HTTPServer(("192.168.100.31",80),HttpProcessor)
	serv.serve_forever()
except:
	#serv.shutdown()
	log("Shutdown")

