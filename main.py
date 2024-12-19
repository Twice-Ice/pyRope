import os
import ctypes
if os.name == "nt": # gets rid of windows global scaling
    ctypes.windll.shcore.SetProcessDpiAwareness(2) 

import pygame
from pygame import Vector2
import globals as gb
from rope import Rope
from point import Point

screen = pygame.display.set_mode((gb.SX, gb.SY), pygame.NOFRAME)

doExit = False
clock = pygame.time.Clock()
rope : Rope = None
point : Point = None

def startGame():
    global rope, point
    startPos = (gb.SX//2, 10)
    rope = Rope(startPos, length=5, thickness=1, segments = 100)
    point = Point(startPos)

startGame()
while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        startGame()
        # screen.fill(gb.BG)

    point.update(screen, [])
    rope.update(screen, point.pos, pygame.mouse.get_rel() if point.grabbed else (0, 0), delta)
    
    pygame.display.flip()
pygame.quit()