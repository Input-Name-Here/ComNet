import pygame
import math
import random
from math import cos,sin

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
		self.fontsize = 11
		self.font = pygame.font.SysFont("Liberation Sans", self.fontsize)
		self.ticks = 0
		self.renderObjs=[]
		self.TPS = 60
		self.camPosX = 0
		self.camPosY = 0
		self.NetObjs = netin
		self.title = ""
		self.bgColour=0,0,0
		self.PPM = 1 # Pixels Per Meter
		self.size = self.width, self.height = w,h
		self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)  # Set Screen
		self.clock = pygame.time.Clock()
		self.leftmouseblock = False
		self.middlemouseblock = False
		self.rightmouseblock = False
	def AddObject(self,obj):
		self.renderObjs.append(obj)
	def setTitle(self,t):
		self.title = t
		pygame.display.set_caption(self.title)
	def RemoveObject(self,obj):
		self.renderObjs.remove(obj)
	def GraphicsTick(self):
		self.ticks +=1
		self.screen.fill(self.bgColour)
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1 # Stop process
			elif event.type == pygame.VIDEORESIZE: # Resize window
				self.size = self.width, self.height = event.dict['size'][0], event.dict['size'][1]
				print(self.size)
			elif event.type == pygame.VIDEOEXPOSE:  # Maximise / Minimise window 
				self.size = self.width, self.height = event.dict['size'][0], event.dict['size'][1]
				print(self.size)

				
		OffX = self.camPosX * self.PPM
		OffY = self.camPosY * self.PPM  

		pygame.mouse.get_pos()

		leftmouse, middlemouse, rightmouse = pygame.mouse.get_pressed()

		if keys[pygame.K_KP4]: 
			self.camPosX+=10/self.PPM
		if keys[pygame.K_KP6]:
			self.camPosX-=10/self.PPM
		if keys[pygame.K_KP8]: 
			self.camPosY+=10/self.PPM
		if keys[pygame.K_KP2]:
			self.camPosY-=10/self.PPM
		if keys[pygame.K_KP7]: 
			self.PPM *=1.1
		if keys[pygame.K_KP1]:
			self.PPM /=1.1
		
		for Obj in self.renderObjs:
			a=math.radians(Obj.icon.angle)
			Obj.PosX+=sin(a)*random.randint(0,4)
			Obj.PosY+=cos(a)*random.randint(0,4)
			Obj.icon.angle+=random.randint(-5,5)

			X=ObjX = (Obj.PosX * self.PPM) + (self.width / 2)+OffX
			Y=ObjY = -(Obj.PosY * self.PPM) + (self.height / 2)+OffY

			if(Obj.circleCheck((ObjX,ObjY),pygame.mouse.get_pos())):
				Obj.colour=(255,255,0)
				Obj.Hover=True
			else:
				Obj.colour=(255,255,255)
				Obj.Hover=False
			if(Obj.Hover and leftmouse and not self.leftmouseblock):
				Obj.Selected=not Obj.Selected
			if(Obj.Selected):
				Obj.colour=(0,255,255)
				if keys[pygame.K_d]: 
					Obj.PosX+=10/self.PPM
				if keys[pygame.K_a]:
					Obj.PosX-=10/self.PPM
				if keys[pygame.K_w]: 
					Obj.PosY+=10/self.PPM
				if keys[pygame.K_s]:
					Obj.PosY-=10/self.PPM
				if keys[pygame.K_LEFT]: 
					Obj.icon.angle-=5
				if keys[pygame.K_RIGHT]:
					Obj.icon.angle+=5

			W = (Obj.icon.width/2)
			H = (Obj.icon.height/2)
			for r in Obj.icon.rects:
				rx= (X-W) + r[0][0] - (r[1][0]/2)
				ry= (Y-H) + r[0][1] - (r[1][1]/2)
				pygame.draw.rect(self.screen, Obj.colour, [ rx, ry, r[1][0], r[1][1] ])
				pygame.draw.rect(self.screen, Obj.colour, [ rx, ry, r[1][0], r[1][1] ])
			for l in Obj.icon.lines:
				a=math.radians(Obj.icon.angle)
				s=1
				x1 = (l[0][0]*s)-W
				y1 = (l[0][1]*s)-H
				x2 = (l[1][0]*s)-W
				y2 = (l[1][1]*s)-H
				lx1= X+( (x1*cos(a)) - (y1*sin(a)) )
				ly1= Y+( (y1*cos(a)) + (x1*sin(a)) )

				lx2 = X+(( x2*cos(a) )- ( y2*sin(a) ))
				ly2 = Y+(( y2*cos(a) )+ ( x2*sin(a) ))
				pygame.draw.aalines(self.screen, Obj.colour, False, ((lx1,ly1),(lx2,ly2)), 2)
			textsurface = self.font.render(Obj.Name, True, Obj.colour)
			self.screen.blit(textsurface, (X+Obj.sizeX, (-1*self.fontsize*1.2)+Y-Obj.sizeY))
			textsurface = self.font.render(Obj.Label, True, Obj.colour)
			self.screen.blit(textsurface, (X+Obj.sizeX, (0*self.fontsize*1.2)+Y-Obj.sizeY))
			textsurface = self.font.render(hex(Obj.ID), True, Obj.colour)
			self.screen.blit(textsurface, (X+Obj.sizeX, (1*self.fontsize*1.2)+Y-Obj.sizeY))
		'''
		for Obj in self.NetObjs:
			ObjX = (Obj.PosX * self.PPM) + (self.width / 2)
			ObjY = -(Obj.PosY * self.PPM) + (self.height / 2)
		

			Obj.scrnpos = ((Obj.PosX * self.PPM) + (self.width / 2) + OffX, -(Obj.PosY * self.PPM) + (self.height / 2) + OffY)


			if(Obj.circleCheck((ObjX,ObjY),pygame.mouse.get_pos())):
				Obj.colour=(255,255,0)
				Obj.colourFill()
				Obj.Hover=True
			else:
				Obj.colour=(150,150,150)
				Obj.Hover=False
				Obj.colourFill()

			if(Obj.Hover and leftmouse and not self.leftmouseblock):
				Obj.Selected=not Obj.Selected

			if(Obj.Selected):
				Obj.colour=(0,255,255)
				Obj.colourFill()
			self.screen.blit(Obj.image, Obj.rect)

		for Obj in self.renderObjs:
			ObjX = (Obj.PosX * self.PPM) + (self.width / 2)
			ObjY = -(Obj.PosY * self.PPM) + (self.height / 2)


			Obj.rect.center = ((Obj.PosX * self.PPM) + (self.width / 2) + OffX, -(Obj.PosY * self.PPM) + (self.height / 2) + OffY)
			if(Obj.circleCheck((ObjX,ObjY),pygame.mouse.get_pos())):
				Obj.colour=(255,255,0)
				Obj.colourFill()
				Obj.Hover=True
			else:
				Obj.colour=(255,255,255)
				Obj.colourFill()
				Obj.Hover=False
			if(Obj.Hover and leftmouse and not self.leftmouseblock):
				Obj.Selected=not Obj.Selected
			if(Obj.Selected):
				Obj.colour=(0,255,255)
				Obj.colourFill()
				if keys[pygame.K_d]: 
					Obj.PosX+=10/self.PPM
				if keys[pygame.K_a]:
					Obj.PosX-=10/self.PPM
				if keys[pygame.K_w]: 
					Obj.PosY+=10/self.PPM
				if keys[pygame.K_s]:
					Obj.PosY-=10/self.PPM
			self.screen.blit(Obj.image, Obj.rect)

		'''


		pygame.draw.lines(self.screen, (255, 255, 255), False,
						((-1, self.height / 2 + OffY), (self.width + 1, self.height / 2 + OffY)), 1)
		pygame.draw.lines(self.screen, (255, 255, 255), False,
						((self.width/2+OffX, -1), (self.width/2+OffX, self.height+1)), 1)
		pygame.display.update() 
		self.leftmouseblock = leftmouse
		self.middlemouseblock = middlemouse
		self.rightmouseblock = rightmouse
		return 0 # Exit cleanly







