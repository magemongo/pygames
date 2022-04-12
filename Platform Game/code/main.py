import pygame, sys
from settings import * 
from level import Level

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
clock = pygame.time.Clock()
level = Level(LEVEL_MAP, screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('black')
	level.run()

	pygame.display.update()
	clock.tick(60)