# Internet Conectivity Module 

import socket
import network as net
from timer import Timer
import time
class INET:
	def __init__(self,i):
		self.hostname = socket.gethostname()
		self.sock = socket.socket()
		self.clientID = i
		self.serverID = 0xFFFF0000

	def connect(self,port):
		self.sock.connect((self.hostname, port))
		self.sock.send(net.CNNC.con("CON",self.serverID,self.clientID))
	def printrecv(self,bytes):
		print("-=- Network Data -=-")
		print(self.sock.recv(bytes))
		print("-=-=-=-=-=--=-=-=-=-")
	def rawrecv(self,bytes):
		return self.sock.recv(bytes)
	def recv(self,bytes):
		rawdata=self.sock.recv(bytes)
		while len(rawdata)==0:
			rawdata =self.sock.recv(bytes)
		return rawdata
	def send(self,bytes):
		return self.sock.send(bytes)
	def waitForSignal(self,bytes,timeout,sig):
		self.sock.settimeout(timeout)
		starttime = time.clock()
		timenow = time.clock()
		while(timenow-starttime<timeout):
			try:
				rawdata = self.sock.recv(bytes)
				if net.decodeAny(rawdata).data == sig:
					self.sock.settimeout(None)
					return 1
				else:
					timenow = time.clock()
			except TimeoutError:
				self.sock.settimeout(None)
				return 0
			except AttributeError:
				timenow = time.clock()
	def waitReturnSignal(self,bytes,timeout,sig):
		self.sock.settimeout(timeout)
		try:
			rawdata = self.sock.recv(bytes)
			if net.decodeAny(rawdata).data == sig:
				return rawdata
			else:
				self.sock.settimeout(None)
				return 1
		except TimeoutError:
			self.sock.settimeout(None)
			return 0

	def disconnect(self):
		self.sock.send(net.CNNC.con("DISCON",self.serverID,self.clientID))
		rtcode = self.waitForSignal(1024,3,"AFF")
		self.sock.close()
		return rtcode

	def close(self):
		self.sock.send(net.CNNC.con("CUTOFF",self.serverID,self.clientID))
		self.sock.close()
	def cutoff(self):
		self.sock.send(net.CNNC.con("CUTOFF",self.serverID,self.clientID))
		self.sock.close()
		
	def die(self):
		self.sock.close()


def waitForSignal(sock,bytes,timeout,sig):
	try:
		rawdata = sock.recv(bytes)

		if net.decodeAny(rawdata).data == sig:
			sock.settimeout(None)
			return 1
	except TimeoutError:
		sock.settimeout(None)
		return 0
def waitReturnSignal(sock,bytes,timeout,sig):
	try:
		rawdata = sock.recv(bytes)
		if net.decodeAny(rawdata).data == sig:
			return rawdata
		else:
			sock.settimeout(None)
			return 1
	except TimeoutError:
		sock.settimeout(None)
		return 0