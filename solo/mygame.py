# necessary imports
import pygame

# main loop keeping the game alive
class Game(object):
	
	def main(self, screen):
		
		# this is a real grown-up game honey, I think it's time it was given a real refresh rate
		clock = pygame.time.Clock()
		
		# bring in player image
		player_image = pygame.image.load('player.png')
		player_image_x = 90
		player_image_y = 300
		
		while True:
			
			# ninety-nine percent sure this means 30 fps
			clock.tick(30)
			
			# TEST INCREMENTER
			player_image_x+=1
			
			for event in pygame.event.get(): # the super listener
				if event.type == pygame.QUIT: # if the red button is pushed
					return # bail
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if ESC is pressed
					return # bail
			
			# fill screen with a nice white... light..... so.... pretty.... 
			screen.fill((241, 241, 241))
			
			# blit our little guy onto the screen wherever we so please!
			screen.blit(player_image, (player_image_x, player_image_y))
			
			# let it snow, let it snow, let it snow
			pygame.display.flip()
		

# starting gun
if __name__ == '__main__':
	
	# pygame off the line
	pygame.init()
	
	# pygame_created_screen off the line
	screen = pygame.display.set_mode((1000, 420))
	
	# game off the line with the screen we just created!
	Game().main(screen)