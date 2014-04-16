# Created by Sahand Nayebaziz
# April 2014, UC Irvine
#
#

# necessary imports
import pygame as pg
import random as rd

# pg off the line
pg.init()

# cave floor class
class Floor:
	length = 0
	height = 0
	x = 0
	y = 0
	
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		

# the starting gun is loaded
def play():
	screen_width = 1000
	screen_height = 420
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	white = (255,255,255)
	black = (0,0,0)
	player_x = 90
	player_y = 100
	player_height = 40
	all_floors = []
	
	clock = pg.time.Clock()
	player_image = pg.image.load('player.png')
	background_image = pg.image.load('bg.png')

	screen = pg.display.set_mode((screen_width, screen_height))

	while True:
		clock.tick(48)
		
		key = pg.key.get_pressed()
		if key[pg.K_SPACE]:
			player_y -= 5
			
		collide = False;
			
		for floor in all_floors:
			if (floor.x < player_x < floor.x + floor.width):
				if player_y < floor.y - player_height:
					collide = False;
				if player_y >= floor.y - player_height:
					collide = True;
					
		if not collide:
			player_y += 3
			

		if all_floors == []:
			all_floors.append(Floor(0, 340, 805, 300))
		else:
			for floor in all_floors:
				if floor.x + floor.width == 800:
					all_floors.append(Floor(1000, rd.randint(200,400), 805, 400))
				if floor.x + floor.width <= 0:
					all_floors.remove(floor)

		screen.fill(white)

		pg.draw.rect(screen, blue, (player_x, player_y, 10, player_height))

		for floor in all_floors:
			floor.x -= 5
			pg.draw.rect(screen, red, (floor.x, floor.y, floor.width, floor.height))
		
		pg.display.update()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				return 
				
		if player_y == screen_height:
			return

play()
	
