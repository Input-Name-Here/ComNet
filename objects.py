import pygame 
import random
class Object: # Generic Object
	def __init__(self):
		self.Name = ""
		self.Label = ""
		self.PosX=0
		self.PosY=0
		self.PosZ=0
		self.ID=random.getrandbits(3*8)
		self.MapDisplay = False
		self.Selected = False # Selected in graphics
		self.Hover = False # Hover over in graphics
		self.colour = (255,255,255)
		self.sizeX = 10 # Pixels
		self.sizeY = 10 # Pixels
		self.scale = 1 # Size Scalar
		self.rect = pygame.Rect((0, 0), (self.sizeX * self.scale, self.sizeY * self.scale))  # Create Rect (pos, size)
		self.image = pygame.Surface((self.sizeX * self.scale, self.sizeY * self.scale))  # Create image (size)
		self.image.fill(self.colour)

	def radiusCheck(self,radius,pos1,pos2): # Radius in pixels, returns true if pos2 is within radius of pos1
		distance = ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
		return distance<=radius

	def update(self,obj):
		self.Name = obj.Name
		self.Label = obj.Label
		self.PosX=obj.PosX
		self.PosY=obj.PosY
		self.PosZ=obj.PosZ
		self.ID=obj.ID
		self.MapDisplay = obj.MapDisplay



	# radius check with automatically calculated radius based on size
	def circleCheck(self,pos1,pos2): 
		radius = 1.1*(((self.sizeX**2)+(self.sizeY**2))**0.5)
		distance = ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
		return distance<=radius

	def arrayExport(self):
		Arr = []
		Arr.append(["ID",str(self.ID)])
		Arr.append(["Name",self.Name])
		Arr.append(["Label",self.Label])
		Arr.append(["PosX",str(self.PosX)])
		Arr.append(["PosY",str(self.PosY)])
		Arr.append(["PosZ",str(self.PosZ)])
		Arr.append(["MapDisplay",str(self.MapDisplay)])
		return Arr
	def arrayImport(Arr):
		newObj = Object()
		newObj.ID=0 # Placeholder null ID
		for i in range(len(Arr)):
			if Arr[i][0] == "ID":
				newObj.ID = int(Arr[i][1])
			if Arr[i][0] == "Name":
				newObj.Name = Arr[i][1]
			if Arr[i][0] == "Label":
				newObj.Label = Arr[i][1]
			if Arr[i][0] == "PosX":
				newObj.PosX = float(Arr[i][1])
			if Arr[i][0] == "PosY":
				newObj.PosY = float(Arr[i][1])
			if Arr[i][0] == "PosZ":
				newObj.PosZ = float(Arr[i][1])
			if Arr[i][0] == "MapDisplay":
				newObj.MapDisplay = bool(Arr[i][1])
		return newObj
	def colourFill(self):
		self.image.fill(self.colour)


		

class MapObject:
	def __init__(self, l,x,y,z):
		self.label = l
		self.PosX=x
		self.PosY=y
		self.PosZ=z
		self.colour = (255,255,255)
		self.sizeX = 10 # Pixels
		self.sizeY = 10 # Pixels
		self.scale = 1 # Size Scalar
		self.rect = pygame.Rect((0, 0), (self.sizeX * self.scale, self.sizeY * self.scale))  # Create Rect (pos, size)
		self.image = pygame.Surface((self.sizeX * self.scale, self.sizeY * self.scale))  # Create image (size)
		self.image.fill(self.colour)
		
