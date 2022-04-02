import random
import colours as c
def Ptype(bytes):
	try:
		return bytes[0:4].decode()
	except:
		print("\n\nPtype ERROR: bytes")

def decodeAny(bytes): 
	if Ptype(bytes)=="CNTP":
		return CNTP.decon(bytes)
	if Ptype(bytes)=="CNNC":
		return CNNC.decon(bytes)


def getAction(Arr):
	Action = ""
	if(Arr[0][0]=="ACT"):
		Action = Arr[0][1]
	return Action


class CN_Data: # recieved data
	def __init__(self,p,v,f,t,o,i,d):
		self.protocol = p
		self.data = d
		self.target = t
		self.origin = o
		self.msgID = i
		self.flags = f
		self.version = v
	def debug(self):
		print("-=- MSG DEBUG -=-")
		print(  "   Protocol:",self.protocol)
		print(   "   Version:",self.version)
		print(     "   Flags:",bin(self.flags))
		print(    "   Target:",hex(self.target))
		print(    "   Origin:",hex(self.origin))
		print("   Message ID:",hex(self.msgID))
		print(      "   Data:",self.data)
		print("-=-=-=-=-=-=-=-=-")
	def getAction(self):
		Arr = self.data
		Action = ""
		if(Arr[0][0]=="ACT"):
			Action = Arr[0][1]
		return Action

def printid(s,i):
	hexid = hex(i)[2:10].upper()
	print(f"{s}{hexid[0:2]}:{hexid[2:4]}:{hexid[4:6]}:{hexid[6:8]}{c.END}")

def formatid(i):
	hexid = hex(i)[2:10].upper()
	return f"{hexid[0:2]}:{hexid[2:4]}:{hexid[4:6]}:{hexid[6:8]}"


class CNTP: # ComNet: Transmission Protocol 
	def con(args,action,target,origin): 
		protocol = "CNTP"
		version = 0
		flags = 0x0000

		args = [["ACT",action]]+args
		EOL = 0b0
		startIndex = 26
		
		msgID = random.getrandbits(6*8)
		bodyBytes = bytes()

		for a in args:
			argLen = len(a[0])
			dataLen = len(a[1])
			bodyBytes += argLen.to_bytes(1, 'big')
			bodyBytes += a[0].encode("utf-8")
			bodyBytes += dataLen.to_bytes(2, 'big')
			bodyBytes += a[1].encode("utf-8")

		endIndex = startIndex+len(bodyBytes)


		msgBytes = bytes()
		headBytes = bytes()
		headBytes += protocol.encode()
		headBytes += startIndex.to_bytes(2, 'big')
		headBytes += endIndex.to_bytes(2, 'big')
		headBytes += version.to_bytes(2, 'big')
		headBytes += flags.to_bytes(2, 'big')
		headBytes += target.to_bytes(4, 'big')
		headBytes += origin.to_bytes(4, 'big')
		headBytes += msgID.to_bytes(6, 'big')

		msgBytes += headBytes
		msgBytes += bodyBytes
		msgBytes += EOL.to_bytes(1, 'big')
		return msgBytes

	def decon(bytes):
		if(bytes[0:4].decode() == "CNTP"):
			if(int.from_bytes(bytes[8:10],"big") == 0 ):
				version = int.from_bytes(bytes[8:10],"big")
				flags = int.from_bytes(bytes[10:12],"big")
				target = int.from_bytes(bytes[12:16],"big")
				origin = int.from_bytes(bytes[16:20],"big")
				msgID = int.from_bytes(bytes[20:26],"big")

				startIndex = int.from_bytes(bytes[4:6],"big")
				endIndex = int.from_bytes(bytes[6:8],"big")
				args = []
				index = startIndex
				while index < endIndex:
					arglen = int.from_bytes(bytes[index:index+1],"big")
					argument = bytes[index+1:index+1+arglen].decode()
					index = index+1+arglen
					datalen = int.from_bytes(bytes[index:index+2],"big")
					data = bytes[index+2:index+2+datalen].decode()
					index = index+2+datalen
					args.append([argument,data])
				return CN_Data("CNTP",version,flags,target,origin,msgID,args)


class CNNC: # ComNet: Network Control
	def con(cmd,target,origin): 
		protocol = "CNNC"
		version = 0
		flags = 0x0000

		
		EOL = 0b0
		startIndex = 26
		
		msgID = random.getrandbits(6*8)
		bodyBytes = bytes()

		cmdLen = len(cmd)
		bodyBytes += cmdLen.to_bytes(1, 'big')
		bodyBytes += cmd.encode("utf-8")

		endIndex = startIndex+len(bodyBytes)


		msgBytes = bytes()
		headBytes = bytes()
		headBytes += protocol.encode()
		headBytes += startIndex.to_bytes(2, 'big')
		headBytes += endIndex.to_bytes(2, 'big')
		headBytes += version.to_bytes(2, 'big')
		headBytes += flags.to_bytes(2, 'big')
		headBytes += target.to_bytes(4, 'big')
		headBytes += origin.to_bytes(4, 'big')
		headBytes += msgID.to_bytes(6, 'big')

		msgBytes += headBytes
		msgBytes += bodyBytes
		msgBytes += EOL.to_bytes(1, 'big')
		return msgBytes

	def decon(bytes):
		if(bytes[0:4].decode() == "CNNC"):
			if(int.from_bytes(bytes[8:10],"big") == 0 ):


				version = int.from_bytes(bytes[8:10],"big")
				flags = int.from_bytes(bytes[10:12],"big")
				target = int.from_bytes(bytes[12:16],"big")
				origin = int.from_bytes(bytes[16:20],"big")
				msgID = int.from_bytes(bytes[20:26],"big")

				startIndex = int.from_bytes(bytes[4:6],"big")
				endIndex = int.from_bytes(bytes[6:8],"big")
				args = []
				index = startIndex
				cmdlen = int.from_bytes(bytes[index:index+1],"big")
				cmd = bytes[index+1:index+1+cmdlen].decode()
				return CN_Data("CNNC",version,flags,target,origin,msgID,cmd)


'''
if len(target) != :
	print("ERROR: CNP:construct, target length invalid")
	raise RuntimeError
if len(target) != :
	print("ERROR: CNP:construct, target length invalid")
	raise RuntimeError
'''