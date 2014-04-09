# necessary imports
import pygame as pg

# pg off the line
pg.init()

# the starting gun is loaded
def play():

	# pg_created_screen off the line with x_size and y_size
	screen = pg.display.set_mode((1000, 420))

	# this is a real grown-up game honey, I think it's time it was given a real refresh rate
	clock = pg.time.Clock()

	# bring in player image
	player_image = pg.image.load('player.png')
	player_x = 90
	player_y = 300

	# watch the world turn
	while True:

		# ninety-nine percent sure this means 30 fps
		clock.tick(30)

		# input listener
		key = pg.key.get_pressed()
		if key[pg.K_LEFT]:
			player_x -= 10
		if key[pg.K_RIGHT]:
			player_x += 10
		if key[pg.K_UP]:
			player_y -= 20
		if key[pg.K_DOWN]:
			player_y += 10

		# gravity mechanics	
		if player_y != 300:
			player_y += 10

		# quit mechanics	
		for event in pg.event.get(): # the super listener
			if event.type == pg.QUIT: # if the red button is pushed
				return # bail
			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: # if ESC is pressed
				return # bail

		# fill screen with a nice white... light..... so.... pretty.... 
		screen.fill((241, 241, 241))

		# blit our little guy onto the screen wherever we so please!
		screen.blit(player_image, (player_x, player_y))

		# let it snow, let it snow, let it snow
		pg.display.flip()

# the starting gun
play()
	
