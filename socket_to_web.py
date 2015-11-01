import json
import threading
import socket
def log(text):
	print text
class LinkToWeb:
	def __init__(self,status_cl, cmd_cl):
		self.status = status_cl
		self.cmd = cmd_cl
		self.wait = True
		self.sock = socket.socket()
		self.sock.bind(('127.0.0.1', 9090))
		self.sock.listen(1)
		try:			
			self.sock.listen(1)
			log("Socket 9090 open")
		except:
			self.wait = False
			log("[Error] to open 9090 socket")
	def start(self):
		log("LinkToWeb.start begin")
		while self.wait:
			try:
				#status = json.loads(standart_json)
				log("Wait to connect")
				self.conn, addr = self.sock.accept()
				data = self.conn.recv(1024)
				try:	
					self.cmd = json.loads(data)	
					if self.cmd['relay'][1]:
						self.relay = self.cmd['relay'][1]							
				except: 
					log("error to decode JSON cmd")
				log ('connected:' + str(addr))
				js_data = json.dumps(self.status)
				self.conn.send(js_data)
				self.conn.close()	
				log("Connect close")
			except:	
				log("[Except] in LinkToWeb.start")
				try:			
					self.conn.close()	
				except:
					log("No conn var in while self.wait:")
				break
		log("LinkToWeb.start end")
	def stop(self):
		self.wait = False
		try:
			self.conn.close()	
		except:
			log("[Except]No conn var in def stop(self):")
		self.sock.shutdown(socket.SHUT_RDWR)
		log("LinkToWeb.Stop")

		
