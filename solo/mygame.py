# BY SAHAND NAYEBAZIZ
# UCI SPRING 2014
#
#

from random import randint
import pygame as pg


############################################################

def process_input():
	game_status = 1
	jump = 0
	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_status = 0 # 0 for game over, 1 for play
	key = pg.key.get_pressed()
	if key[pg.K_UP]:
		jump = 1
	elif key[pg.K_ESCAPE]:
		game_status = 0

	return game_status, jump

############################################################

def draw_everything(screen, player, floors):
    screen.fill((32, 32, 32))

    pg.draw.rect(screen, (255, 255, 255), (player['x'], player['y'], player['width'], player['height']))

    for key in floors:
    	pg.draw.rect(screen, (90, 90, 90), (key, floors[key][0], floors[key][1], 600))
    
    pg.display.update()

############################################################

def create_player():
	player = {'x': 20, 'y': 100, 'width': 7, 'height': 30}
	return player

############################################################

def move_player(player, jump, jump_start, jump_time):
	if jump:
		if jump_time == 0:
			jump_start = pg.time.get_ticks() + 1
			player['y'] -= 3
			jump_time = 1
		if jump_time < 600:
			player['y'] -= 2
			jump_time = pg.time.get_ticks() - jump_start

	if not jump:
		jump_start = 0
		jump_time = 0
		player['y'] += 3

	return player, jump_start, jump_time


############################################################

def create_floors():
	floors = {}
	return floors

############################################################

def move_floors(floors):
	if len(floors) == 0:
		floors = {0: (140, 100)}
	if len(floors) != 0:
		for key in floors:
			floors[key - 1] = (floors[key][0], floors[key][1])
			del floors[key]
	return floors

############################################################

pg.init()
clock = pg.time.Clock()

# display
dims = 480, 160
screen = pg.display.set_mode(dims)

# game objects
player = create_player()
floors = create_floors()

# game loop
game_status = 1  # 0 for game over, 1 for play
jump_start = 0
jump_time = 0
while game_status:

	game_status, jump = process_input()
	
	player, jump_start, jump_time = move_player(player, jump, jump_start, jump_time)
	floors = move_floors(floors)

	draw_everything(screen, player, floors)
    
	clock.tick(50)  # or sleep(.02) to have the loop pg-independent