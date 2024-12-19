import pygame
from pygame import Vector2
import math
import globals as gb

def pointOnScreen(pos, camera : Vector2 = (0, 0), size : float = 1):
		ssPoint = pos + camera #screen space point. Converts pos from ws to ss.
		size = abs(size) #only ever should be a positive value.
		if ssPoint.x + size > 0 and ssPoint.x - size < gb.SX and ssPoint.y + size > 0 and ssPoint.y - size < gb.SY:
			return True
		else:
			return False

class Point:
	def __init__(self, pos : Vector2 = Vector2(0, 0), color : tuple = (255, 255, 255)):
		self.pos = Vector2(pos)
		self.staticPos = pos
		self.color = color
		self.size = 2
		self.active = True
		self.grabbed = False
		self.highlighted = False
	
	#staticPos is the position of the point when it was last grabbed.
	#grabbed points is a list of all points that are held. This is to prevent holding more than one point when adjusting all points.
	def update(self, screen : pygame.surface, grabbedPoints : list, camera : Vector2 = (0, 0)): #draw : bool = True):
		keys = pygame.key.get_pressed()
		maxGrabbed = 1 if not keys[pygame.K_LSHIFT] else 2

		mousePos = Vector2(pygame.mouse.get_pos())
		if math.dist(mousePos, self.pos + camera) <= 5 and len(grabbedPoints) < maxGrabbed: #if the mouse is in range to grab this point and isn't already grabbing a point.
			self.highlighted = True
			if pygame.mouse.get_pressed(3)[0] and not self.grabbed: #if the point is clicked on.
				self.grabbed = True
				grabbedPoints.append(self) #adds itself to the list of all grabbed points.
		elif not self.grabbed: #only will set self.highlighted to False if the point isn't grabbed AND the mouse isn't in range of the point.
			self.highlighted = False

		#if the mouse was close enough to activate the highlighted bool, then the point will be slightly larger.
		#having the code seperate allows for the particle to appear highlighted even though it's not technically in distance because the mouse moves too fast.
		if self.highlighted: 
			self.size = 5 #size when held
		else:
			# self.size = math.dist(mousePos, self.pos + camera)
			self.size = 2 #default size if it's not grabbed.

		if self.active:
			if self.grabbed:
				self.pos = mousePos - camera
				if not pygame.mouse.get_pressed(3)[0]: #when lmb is released. (only calls once)
					self.grabbed = False
					self.highlighted = False
					self.pos = mousePos - camera #position is updated
					self.staticPos = self.pos #updates staticPos
					if self in grabbedPoints:
						grabbedPoints.remove(self) #removed from list of held points.
				if self.pos.x > gb.SX:
					self.pos.x = gb.SX
				pygame.draw.circle(screen, self.color, self.pos + camera, self.size) #draws to self.pos, which == mousePos
			elif pointOnScreen(self.pos, camera, self.size): #culls points when off screen
				#if the point isn't being held by the mouse, then it's position is set to it's position in the world space.
				pygame.draw.circle(screen, self.color, self.pos + camera, self.size)
	
	def updateStaticPos(self):
		self.staticPos = self.pos

	def setPos(self, pos):
		self.pos = pos
		self.updateStaticPos()