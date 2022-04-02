import pygame


def Screen2World(t):
	x,y = t
	global height
	global width
	global PPM
	global camPosY
	global camPosX
	x = ((x-width/2)/PPM)-camPosX
	y = ((-y+height/2)/PPM)+camPosY
	return (x,y)

def World2Screen(t):
	x,y = t
	global height
	global width
	global PPM
	global camPosY
	global camPosX
	x = (x*PPM)+(camPosX * PPM) + (width/2)
	y = (-y*PPM)+(camPosY * PPM) + (height/2)
	return (x,y)

class MapWindow: 
	def __init__(self,h,w,netin):
		pygame.init()
		pygame.font.init()
		self.ticks = 0
		self.renderObjs=[]
		self.TPS = 60
		self.camPosX = 0
		self.camPosY = 0
		self.NetObjs = netin

		self.bgColour=0,0,0
		self.PPM = 1 # Pixels Per Meter
		self.size = self.width, self.height = w,h
		self.screen = pygame.display.set_mode(self.size)  # Set Screen
		self.clock = pygame.time.Clock()

	def AddObject(self,obj):
		self.renderObjs.append(obj)
	def RemoveObject(self,obj):
		self.renderObjs.remove(obj)
	def GraphicsTick(self):
		self.ticks +=1
		self.screen.fill(self.bgColour)
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1 # Stop process
		OffX = self.camPosX * self.PPM
		OffY = self.camPosY * self.PPM  

		pygame.mouse.get_pos()


		if keys[pygame.K_KP4]: 
			self.camPosX+=10/self.PPM
		if keys[pygame.K_KP6]:
			self.camPosX-=10/self.PPM
		if keys[pygame.K_KP8]: 
			self.camPosY+=10/self.PPM
		if keys[pygame.K_KP2]:
			self.camPosY-=10/self.PPM
		


		for Obj in self.NetObjs:
			ObjX = (Obj.PosX * self.PPM) + (self.width / 2)
			ObjY = -(Obj.PosY * self.PPM) + (self.height / 2)
		

			Obj.rect.center = ((Obj.PosX * self.PPM) + (self.width / 2) + OffX, -(Obj.PosY * self.PPM) + (self.height / 2) + OffY)
			if(circleCheck((ObjX,ObjY),pygame.mouse.get_pos())):
				Obj.colour=(255,255,0)
				Obj.colourFill()
			else:
				Obj.colour=(255,255,255)
				Obj.colourFill()
			self.screen.blit(Obj.image, Obj.rect)

		for Obj in self.renderObjs:
			ObjX = (Obj.PosX * self.PPM) + (self.width / 2)
			ObjY = -(Obj.PosY * self.PPM) + (self.height / 2)


			Obj.rect.center = ((Obj.PosX * self.PPM) + (self.width / 2) + OffX, -(Obj.PosY * self.PPM) + (self.height / 2) + OffY)
			if(circleCheck((ObjX,ObjY),pygame.mouse.get_pos())):
				Obj.colour=(255,255,0)
				Obj.colourFill()
			else:
				Obj.colour=(200,200,200)
				Obj.colourFill()
			self.screen.blit(Obj.image, Obj.rect)

		pygame.draw.lines(self.screen, (255, 255, 255), False,
						((-1, self.height / 2 + OffY), (self.width + 1, self.height / 2 + OffY)), 1)
		pygame.draw.lines(self.screen, (255, 255, 255), False,
						((self.width/2+OffX, -1), (self.width/2+OffX, self.height+1)), 1)
		pygame.display.update() 
		return 0 # Exit cleanly







