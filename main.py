import network as net
import random
import inet
import sys
import pygame
import objects
import time
import colours as c
import graphics
import random
from threading import Thread, Lock

'''
INFORMATION:
Arguments:
	--regen-id / -ri : Use a custom ID
	--no-write-id / -nwi : Do not write ID to disk  
'''



print(f"Main: {c.GREEN}START{c.END}")
print("-=-=- Setup -=-=-")
port = 1248 # Default port
ports = [1248,1249,1250,1251] # Alternative ports list

verbose = False
IDblackList = [] # List of known IDs to not use 
clientBlock = 0xB1
netID = 0

serverID = 0

timeouts = 5 # Number of extra connections before stopping
timeoutdelay = 0.1 # Connection attempt delay


if("--regen-id " in sys.argv or "-ri" in sys.argv):
	print("Regenerating ID")
	while netID == 0 or netID in IDblackList:
		netID = (clientBlock<<24)+(random.getrandbits(3*8))
	if not ("--no-write-id " in sys.argv or "-nwi" in sys.argv):
		with open("clientid.txt", "w") as f:
			f.write( hex(netID) )
		print("Client ID written to disk")
else:
	try:
		print("Using historic ID")
		with open("clientid.txt", "r") as f:
			netID = int(f.read(),0)
	except:
		print("No ID found, generating...")
		while netID == 0 or netID in IDblackList:
			netID = (clientBlock<<24)+(random.getrandbits(3*8))
		if not ("--no-write-id " in sys.argv or "-nwi" in sys.argv):
			with open("clientid.txt", "w") as f:
				f.write( hex(netID) )
			print("Client ID written to disk")

net.printid(f"Client ID: {c.BLUE}",netID)
print("-=-=- End of Client setup -=-=-")
connected = False

attemptConnect = True
for p in ports:
	timeoutcounter=0
	port = p
	while attemptConnect:
		try:
			print(f"Attempting connection {c.BLUE}{timeoutcounter}{c.END} on port {c.BLUE}{port}{c.END}",end="\r")
			iC = inet.INET(netID)
			iC.connect(port)
			print()
			if(verbose):
				net.printid(f'\n{c.YELLOW}SEND{c.END}: {c.PURPLE}CON{c.END} to {c.BLUE}', 0xFFFF0000)

			'''
			rawdata = iC.waitForSignal(1024,3,"")
			data = net.decodeAny(rawdata)
			if verbose:
				net.printid(f'{c.CYAN}RECV{c.END}: {c.PURPLE}{data.data}{c.END} from {c.BLUE}', data.origin)
			serverID = data.origin
			print(f"Connected {c.GREEN}successfully{c.END}")
			connected = True
			attemptConnect = False
			break
			'''
			rawdata = iC.waitReturnSignal(1024,3,"ACK")
			if(rawdata!=0):

				data = net.decodeAny(rawdata)
				if verbose:
					net.printid(f'{c.CYAN}RECV{c.END}: {c.PURPLE}{data.data}{c.END} from {c.BLUE}', data.origin)
				serverID = data.origin
				if verbose:
					print(f"Connected {c.GREEN}successfully{c.END}")
				connected = True
				attemptConnect = False
				break
			else:
				print(f"{c.YELLOW}Timeout:{rawdata} {c.END}")

		except Exception as e:
			if verbose:
				print(e)
			time.sleep(timeoutdelay)
		if(timeoutcounter >= timeouts):
			if verbose:
				print(f"\nConnection {c.RED}timed out{c.END}")
			break
		timeoutcounter+=1
	if connected:
		break


if (not connected):
	print(f"\nRunning with network?: {c.RED}No{c.END}")
else:
	print(f"Running with network?: {c.GREEN}Yes{c.END}")
	net.printid(f"Server ID: {c.BLUE}",serverID)




thrLock = Lock()






print("-=-=- End of setup -=-=-")


#net.CNTP.con()

sex = objects.Object()
sex.PosX=random.randint(-100,100)
sex.PosY=random.randint(-100,100)
sex.Name = "sex"
sex.Label = "SuperSexy"
sex.MapDisplay= True
netOutObjs=[sex]
netInObjs=[]
Map = graphics.MapWindow(512,512,netInObjs)
Map.AddObject(sex)

RunThreads = [True] # Uses list so it can be passed to threads
                    # Boolean get passed by value, not reference. 

def networkRecvThreadFunc(lock, iC):
	print(f"NetworkRecv: {c.GREEN}START{c.END}")
	global RunThreads
	global netInObjs
	global netOutObjs
	global connected
	try:
		while RunThreads[0]:
			try:
				if connected:
					ack=True
					lock.acquire()
					rawdata=iC.recv(1024)
					lock.release()

					
					if verbose:
						print(f"Raw Data: {c.YELLOW}{rawdata}{c.END}")
					if len(rawdata)==0:
						print(f"{c.LIGHT_RED}Client {c.BLUE}{net.formatid(clientID)}{c.LIGHT_RED} forcefully disconnected[2]{c.END}")
						iC.die()
						break
					data = net.decodeAny(rawdata)
					if verbose:
						net.printid(f'{c.YELLOW}RECV: {c.PURPLE}{data.data}{c.END} from {c.BLUE}', data.origin)
					if data.protocol=="CNTP":
						if data.getAction() == "UPDATE":
							print("yo")
							if verbose:
								print("ACTION: Updating object tables")
							newObj = objects.Object.arrayImport(data.data)
							updated=False
							for i in range(len(netInObjs)): 
								if(netInObjs[i].ID == newObj.ID):
									if verbose:
										print(f"Update to OBJ {c.BLUE}{hex(newObj.ID)}{c.END}")
									lock.acquire()
									netInObjs[i].update(newObj)
									lock.release()
									updated = True
							if(not updated):
								lock.acquire()
								netInObjs.append(newObj)
								lock.release()
								if verbose:
									print(f"Added OBJ {c.BLUE}{hex(newObj.ID)}{c.END} to table")
						elif data.getAction() == "GETOBJS":
							print(f"NetworkTick: {c.YELLOW}ERROR: NOT IMPLEMENTED{c.END}          ")
							ack=False
					elif data.protocol=="CNNC":
						if data.data=="DISCON":
							print(f"NetworkTick: {c.YELLOW}ERROR: NOT IMPLEMENTED{c.END}          ")
							ack=False
						if data.data=="CUTOFF":
							print(f"NetworkTick: {c.YELLOW}ERROR: NOT IMPLEMENTED{c.END}          ")
							ack=False
						if data.data=="ACK":
							ack=False
					if ack:
						iC.send(net.CNNC.con("ACK",data.origin,netID))
						if verbose:
							net.printid(f'{c.CYAN}SEND:  {c.PURPLE}ACK{c.END} to {c.BLUE}', data.origin)

				else:
					time.sleep(1/30)
			except BlockingIOError:
				print(f"NetworkRecv: {c.YELLOW}WARN: RECV Blocked{c.END}          ")
	except Exception as e:
		print(f"NetworkRecv: {c.YELLOW}ERROR: {e}{c.END}          ")
	print(f"NetworkRecv: {c.RED}STOP{c.END}          ")


def networkTickThreadFunc(lock, iC):
	print(f"NetworkTick: {c.GREEN}START{c.END}")
	global RunThreads
	global connected
	global netInObjs
	global netOutObjs
	try:
		while RunThreads[0]:
			if connected:
				counter = 0
				for o in netOutObjs:
					counter+=1
					iC.send(net.CNTP.con(o.arrayExport(),"UPDATE",serverID,netID))
					#iC.waitForSignal(1024,1,"ACK")
					time.sleep(1/30)
					iC.send(net.CNTP.con([],"GETOBJS",serverID,netID))
				#print(f"Server sent {counter} object updates",end="\r")
				time.sleep(1/30)
			else:
				time.sleep(1/30)
	except BrokenPipeError as e:
		print(f"NetworkTick: {c.YELLOW}ERROR: BROKEN PIPE{c.END}          ")
		print(f"NetworkTick: {c.LIGHT_CYAN}FORCE DISCONNECT{c.END} ")
		print(f"NetworkTick: {c.RED}STOP{c.END}          ")
		iC.die()
		return
	except Exception as e:
		print(f"NetworkTick: {c.YELLOW}ERROR: {e}{c.END}          ")

	if(connected):
		print(f"NetworkTick: {c.LIGHT_CYAN}DISCONNECT: INITIATE{c.END}          ")
		rtc = iC.disconnect()
		if verbose:
			print(f"NetworkTick: {c.LIGHT_CYAN}DISCONNECT: RTC[{rtc}]{c.END}          ")
		print(f"NetworkTick: {c.LIGHT_CYAN}DISCONNECT: SUCCESS{c.END}          ")
	print(f"NetworkTick: {c.RED}STOP{c.END}          ")


def graphicsThreadFunc(lock,Map):
	global RunThreads
	print(f"Graphics: {c.GREEN}START{c.END}")
	try:
		while RunThreads[0]:
			if(Map.GraphicsTick()): # If return 1, exit
				break
			time.sleep(1/Map.TPS)
	except Exception as e:
		print(f"Graphics: {c.YELLOW}ERROR: {e}{c.END}")
	print(f"Graphics: {c.RED}STOP{c.END}")


graphicsThread = Thread(target=graphicsThreadFunc,args=(thrLock ,Map))
graphicsThread.start()

networkTickThread = Thread(target=networkTickThreadFunc,args=(thrLock, iC))
networkTickThread.start()

networkRecvThread = Thread(target=networkRecvThreadFunc,args=(thrLock, iC))
networkRecvThread.start()

graphicsThread.join()
#input("Main: Running without graphics, press ENTER to exit")

print(f"Main: {c.YELLOW}Detected shutdown, waiting for threads to close...{c.END}")


thrLock.acquire()
RunThreads=[False]
thrLock.release()
networkTickThread.join()


print(f"Main: {c.RED}STOP{c.END}")