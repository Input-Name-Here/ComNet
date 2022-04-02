import socket               # Import socket module
import network as net
import random
import sys
import objects
import colours as c
import inet
from threading import Thread, Lock
import time 

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1248                # Default port
ports = [1248,1249,1250,1251] # List of all used ports
RunThreads=[True]
verbose = True # Print extra debug data
verboseraw = False
serverBlock = 0xA1
netID = 0
IDblackList=[]
thrLock = Lock()
SendDelay=20/1000 # Milliseconds
objs = []

if("--regen-id " in sys.argv or "-ri" in sys.argv):
	print("Regenerating ID")
	while netID == 0 or netID in IDblackList:
		netID = (serverBlock<<24)+(random.getrandbits(3*8))
	if not ("--no-write-id " in sys.argv or "-nwi" in sys.argv):
		with open("serverid.txt", "w") as f:
			f.write( hex(netID) )
		print("Network ID written to disk")
else:
	try:
		print("Using historic ID")
		with open("serverid.txt", "r") as f:
			netID = int(f.read(),0)
	except:
		print("No ID found, generating...")
		while netID == 0 or netID in IDblackList:
			netID = (serverBlock<<24)+(random.getrandbits(3*8))
		if not ("--no-write-id " in sys.argv or "-nwi" in sys.argv):
			with open("serverid.txt", "w") as f:
				f.write( hex(netID) )
			print("Network ID written to disk")
net.printid(f"Network ID: {c.BLUE}",netID)



def ConnectionHandler(lock, con,addr):
	global RunThreads
	global objs
	global SendDelay
	Run = True
	rawdata=inet.waitReturnSignal(con,1024,3,"CON")
	if verbose:
		print(f"TCP Connection from {c.BLUE}{addr}{c.END}")
	if(type(rawdata)!=int):
		data = net.decodeAny(rawdata)
		if verbose:
			net.printid(f'{c.YELLOW}RECV: {c.PURPLE}{data.data}{c.END} from {c.BLUE}', data.origin)
		clientID = data.origin
		con.send(net.CNNC.con("ACK",clientID,netID))
							
		print(f"Client {c.BLUE}{net.formatid(clientID)} {c.GREEN}Connected{c.END}")
		while RunThreads[0] and Run:
			try:
				ack = True

				rawdata=con.recv(1024)
				if verbose and verboseraw:
					print(f"Raw Data: {c.YELLOW}{rawdata}{c.END}")
				if len(rawdata)==0:
					print(f"Client {c.BLUE}{net.formatid(clientID)}{c.LIGHT_RED} forcefully disconnected [NO DATA]{c.END}")
					con.close()
					break

				data = net.decodeAny(rawdata)
				if verbose:
					net.printid(f'{c.YELLOW}RECV: {c.PURPLE}{data.data}{c.END} from {c.BLUE}', data.origin)
				if data.protocol=="CNTP":
					if data.getAction() == "UPDATE":
						if verbose:
							print("ACTION: Updating object tables")
						newObj = objects.Object.arrayImport(data.data)
						updated=False
						print(objs)
						for i in range(len(objs)): 
							print(i,objs[i].ID,newObj.ID)
							if(objs[i].ID == newObj.ID):
								
								if verbose or True:
									print(f"Update to OBJ {c.BLUE}{hex(newObj.ID)}{c.END}")
								updated = True
								lock.acquire()
								objs[i].update(newObj)
								lock.release()
						if(not updated):
							lock.acquire()
							objs.append(newObj)
							lock.release()
							if verbose or True:
								print(f"Added OBJ {c.BLUE}{hex(newObj.ID)}{c.END} to table")
					elif data.getAction() == "GETOBJS":
						ack=False
						for o in objs:
							con.send(net.CNTP.con(o.arrayExport(),"UPDATE",clientID,netID))
							#while inet.waitForSignal(con,1024,1,"ACK") == 0:
							time.sleep(SendDelay)
								#inet.send(con,net.CNTP.con(o.arrayExport(),"UPDATE",clientID,netID))
							if verbose:
								net.printid(f'{c.CYAN}SEND: {c.PURPLE}UPDATE: {c.LIGHT_PURPLE}{o.arrayExport()}{c.END} to {c.BLUE}', data.origin)
							#time.sleep(SendDelay)

				elif data.protocol=="CNNC":
					if data.data=="DISCON":
						ack=False
						print(f"Client {c.BLUE}{net.formatid(clientID)}{c.RED} disconnected [DISCON]{c.END}")
						con.send(net.CNNC.con("AFF",data.origin,netID))
						if verbose:
							net.printid(f'{c.CYAN}SEND: {c.PURPLE}AFF{c.END} to {c.BLUE}', data.origin)
						con.close()
						Run = False
						break
					if data.data=="CUTOFF":
						ack=False
						print(f"Client {c.BLUE}{net.formatid(clientID)}{c.RED} disconnected [CUTOFF]{c.END}")
						con.close()
						Run = False
						break
					if data.data=="ACK":
						ack=False
				if ack:
					con.send(net.CNNC.con("ACK",data.origin,netID))
					if verbose:
						net.printid(f'{c.CYAN}SEND:  {c.PURPLE}ACK{c.END} to {c.BLUE}', data.origin)

			except BrokenPipeError as e:
				print(f"Client {c.BLUE}{net.formatid(clientID)}{c.LIGHT_RED} forcefully disconnected [BROKEN PIPE]{c.END}")
				con.close()
				break
			except TimeoutError as e:
				if verbose:
					print(f"Error processing data: {c.RED}{e}{c.END}")
					con.close()
					break
			except Exception as e:
				if verbose:
					print(f"Error processing data: {c.RED}{e}{c.END}")
	elif(rawdata==0 and verbose ):
		print(f"TCP {c.BLUE}{addr}{c.LIGHT_RED} connect attempt failed [TIMEOUT]{c.END}")
	elif(verbose):
		print(f"TCP {c.BLUE}{addr}{c.LIGHT_RED} connect attempt failed [INVALID SIGNAL]{c.END}")
	con.close()  

for p in ports:
	port = p
	print(f"Attempting setup on port {c.BLUE}{port}{c.END}      ",end="\r")
	try:
		s.bind((host, port))        # Bind to the port
		print(f"\nBound on port {c.BLUE}{port}{c.END}")
		break
	except Exception as e:
		time.sleep(1)




s.listen(10)                 # Now wait for client connection.
threads=[]
print("\n-=- End of setup -=-\n")

try:
	while True:
		con, addr = s.accept()     # Establish connection with client.

		threads.append(Thread(target=ConnectionHandler,args=(thrLock,con,addr)))
		threads[-1].start()
except:
	RunThreads=[False]
		

for t in threads:
	t.join()

