import pygame
from pygame import Vector2
import globals as gb
import numpy as np

class Rope:
    def __init__(self,
                 pos : Vector2|tuple = (0, 0),
                 length : float = 5,
                 color : tuple = (255, 255, 255),
                 thickness : int = 2,
                 segments : int = 100,
                 _firstSegment : bool = True):
        self.length = length
        self.p1 = Vector2(pos)
        self.p2 = None
        self.p2Angle(0)
        self.color = color
        self.thickness = thickness
        self.velo = Vector2(0, 0)
        self.child = Rope(self.p2, length, color, thickness, segments - 1, False) if segments > 0 else None
        self._firstIteration = _firstSegment

    def moveP2(self,
               newPos : Vector2|tuple = None):
        '''moves p2 to where it has been pulled to based on it's parent rope position'''
        midPoint = self.p2 + (self.p1 - self.p2) * .5
        if newPos != None:
            self.p1 = Vector2(newPos)
        angle = np.atan2(midPoint.y - self.p1.y, midPoint.x - self.p1.x)
        self.p2Angle(angle)

    def applyVelo(self,
                  delta : float = 0.015):
        '''moves p2 to where it should be based on the velo'''
        point = self.p2 + self.velo * delta
        angle = np.atan2(point.y - self.p1.y, point.x - self.p1.x)
        self.p2Angle(angle)

        newAngle = np.atan2(self.p2.y - self.p1.y, self.p2.x - self.p1.x)
        deltaAngle = newAngle - angle

        veloDist = np.sqrt((self.velo.x)**2 + (self.velo.y)**2)
        veloAngle = np.atan2(self.velo.y, self.velo.x)

        veloAngle += deltaAngle/2

        self.velo = Vector2(veloDist * np.cos(veloAngle), veloDist * np.sin(veloAngle))

    def p2Angle(self,
                angle : float = 0):
        '''interpolates p2 based on the inputed angle (in rads).'''
        self.p2 = self.p1 + Vector2(np.cos(angle), np.sin(angle)) * self.length

    def gravity(self):
        '''applies gravity'''
        self.velo += Vector2(0, 200)

    def inheritVelo(self,
                    parentVelo : Vector2|tuple = (0, 0)):
        '''Inherits parent rope velo'''
        self.velo = self.velo/2 + Vector2(parentVelo)/2

    def draw(self,
             screen : pygame.Surface):
        '''draws rope segment'''
        if self._firstIteration:
            pygame.draw.circle(screen, (255, 255, 255), self.p1, 2)
        pygame.draw.line(screen, self.color, self.p1, self.p2, self.thickness)
        if self.thickness > 1:
            pygame.draw.circle(screen, self.color, self.p1, self.thickness//2)
            pygame.draw.circle(screen, self.color, self.p2, self.thickness//2)

    def update(self,
               screen : pygame.Surface,
               newPos : Vector2|tuple = (0, 0),
               parentVelo : Vector2|tuple = (0, 0),
               delta : float = 0.015):
        self.gravity()
        self.moveP2(newPos)
        self.applyVelo(delta)
        self.inheritVelo(parentVelo)

        self.draw(screen)

        if self.child:
            self.child.update(screen, self.p2, self.velo, delta)