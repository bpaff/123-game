# necessary imports
import pygame

# pygame off the line
pygame.init()

# the starting gun is loaded
def play():

	# pygame_created_screen off the line
	screen = pygame.display.set_mode((1000, 420))

	# this is a real grown-up game honey, I think it's time it was given a real refresh rate
	clock = pygame.time.Clock()

	# bring in player image
	player_image = pygame.image.load('player.png')
	player_x = 90
	player_y = 300

	# watch the world turn
	while True:

		# ninety-nine percent sure this means 30 fps
		clock.tick(30)

		# input listener
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			player_x -= 10
		if key[pygame.K_RIGHT]:
			player_x += 10
		if key[pygame.K_UP]:
			player_y -= 20
		if key[pygame.K_DOWN]:
			player_y += 10

		# gravity mechanics	
		if player_y != 300:
			player_y += 10

		# quit mechanics	
		for event in pygame.event.get(): # the super listener
			if event.type == pygame.QUIT: # if the red button is pushed
				return # bail
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if ESC is pressed
				return # bail

		# fill screen with a nice white... light..... so.... pretty.... 
		screen.fill((241, 241, 241))

		# blit our little guy onto the screen wherever we so please!
		screen.blit(player_image, (player_x, player_y))

		# let it snow, let it snow, let it snow
		pygame.display.flip()

# the starting gun
play()
	
