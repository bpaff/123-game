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
	blue = (0,0,255)
	white = (255,255,255)
	player_x = 90
	player_y = 100
	player_width = 10
	player_height = 40
	all_floors = []

	player_image = pg.image.load('player.png')
	background_image = pg.image.load('bg.png')

	screen = pg.display.set_mode((screen_width, screen_height))
	clock = pg.time.Clock()

	while True:
		#fps
		clock.tick(48)
		
		# jump
		key = pg.key.get_pressed()
		if key[pg.K_SPACE]:
			player_y -= 5

		# gravity
		collide_x = False;
		collide_y = False;
		for floor in all_floors:
			if (floor.x < player_x < floor.x + floor.width):
				if player_y < floor.y - player_height:
					collide_y = False;
				if player_y >= floor.y - player_height:
					collide_y = True;
			if (player_y > floor.y - player_height) and (player_x + player_width < floor.x):
				player_x
		if not collide_y:
			player_y += 3
			
		# floor logic	
		if all_floors == []:
			all_floors.append(Floor(0, 340, 805, 300))
		else:
			for floor in all_floors:
				if floor.x + floor.width == 800:
					all_floors.append(Floor(1000, rd.randint(200,400), 805, 400))
				if floor.x + floor.width <= 0:
					all_floors.remove(floor)

		# draw background, floors, and player
		screen.blit(background_image, (0,0))
		pg.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))
		for floor in all_floors:
			floor.x -= 5
			pg.draw.rect(screen, white, (floor.x, floor.y, floor.width, floor.height))
		
		# update
		pg.display.update()
		
		# quit
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				return 
		if player_y == screen_height:
			return

play()
	
