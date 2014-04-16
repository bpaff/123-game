# Created by Sahand Nayebaziz
# April 2014, UC Irvine
#
#

# necessary imports
import pygame as pg
import random as rd

# pg off the line
pg.init()

# the starting gun is loaded
def play():

	# display information
	screen_width = 1000
	screen_height = 420

	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	darkBlue = (0,0,128)
	white = (255,255,255)
	black = (0,0,0)
	pink = (255,200,200)

	# create a screen off the line with x_size and y_size
	screen = pg.display.set_mode((screen_width, screen_height))

	# get ready for refresh rate
	clock = pg.time.Clock()

	# bring in player image
	player_image = pg.image.load('player.png')
	background_image = pg.image.load('bg.png')
	player_x = 90
	player_y = 300 
	floor_x = 1000
	floor_y = 340

	# speed of advancement
	dx = 1.6

	# empty list of floor lengths
	floor_lengths = []

	# floor counter
	floor_counter = 0

	# watch the world turn
	while True:
		
		# ninety-nine percent sure this means 30 fps
		clock.tick(40)

		# make a new floor
		floor_lengths.append(rd.randint(200, 600))

		# input listener
		key = pg.key.get_pressed()
		if key[pg.K_UP]:
			player_y -= 9
		if key[pg.K_DOWN]:
			player_y += 10

		# gravity mechanics	
		if player_y != 300:
			player_y += 3

		# move floors
		floor_x -= dx

		# quit mechanics	
		for event in pg.event.get(): # the super listener
			if event.type == pg.QUIT: # if the red button is pushed
				return # bail
			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: # if ESC is pressed
				return # bail

		# fill screen with a nice white... light..... so.... pretty.... 
		screen.blit(background_image, (0,0))

		# draw player
		pg.draw.rect(screen,blue,(player_x, player_y, 10, 40))

		# draw a floor
		pg.draw.rect(screen, red,(floor_x - 900, floor_y, 700, 20))
		pg.draw.rect(screen, red,(floor_x, floor_y, 400, 20))
		pg.draw.rect(screen, red,(floor_x + 500, floor_y, 400, 20))
		pg.draw.rect(screen, red,(floor_x + 1000, floor_y, 400, 20))
		pg.draw.rect(screen, red,(floor_x + 1500, floor_y, 400, 20))
		
		# let it snow, let it snow, let it snow
		pg.display.update()

		# slowly speed up
		dx = dx * 1.006

# the starting gun
play()
	
