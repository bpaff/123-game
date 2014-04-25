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
	player = {'x': 60, 'y': 40, 'width': 7, 'height': 30}
	return player

############################################################

def move_player(player, jump, jump_start, jump_time, floors, falling):
	if falling:
		jump = False

	if not jump:
		falling = True
		jump_start = 0
		jump_time = 0
		player['y'] += 4

	if not falling:
		if jump:
			if jump_time == 0:
				jump_start = pg.time.get_ticks() + 1
				player['y'] -= 10
				jump_time = 1
			elif jump_time <= 50:
				player['y'] -= 7.7
				jump_time = pg.time.get_ticks() - jump_start
			elif jump_time < 100:
				player['y'] -= 5.2
				jump_time = pg.time.get_ticks() - jump_start
			elif jump_time < 200:
				player['y'] -= 3.0
				jump_time = pg.time.get_ticks() - jump_start
			elif jump_time < 260:
				player['y'] -= .9
				jump_time = pg.time.get_ticks() - jump_start
			elif jump_time >= 260:
				falling = True
	
	for key in floors:
		player_rect_collide = pg.Rect(key, floors[key][0], floors[key][1], 600).colliderect(pg.Rect(player['x'], player['y'], player['width'], player['height']))
		if player_rect_collide:
			if player['x'] > key:
				falling = False

	for key in floors:
		player_rect_collide = pg.Rect(key, floors[key][0], floors[key][1], 600).colliderect(pg.Rect(player['x'], player['y'], player['width'], player['height']))
		if player_rect_collide:
			if player['x'] > key:
				player['y'] = floors[key][0] - player['height']
			elif (player['y'] + player['height']) >= floors[key][0]:
				player['x'] = key - player['width']


	return player, jump_start, jump_time, falling


############################################################

def create_floors():
	floors = {0: (100, 420)} # floors is a dict with key x-coord and value (y-coord, width)
	return floors

############################################################

def move_floors(floors, motion):
	floor_needed = True
	floors_new = {}

	if len(floors) != 0:
		for key in floors:
			if (key + floors[key][1]) > randint(420, 460):
				floor_needed = False

		for key in floors:
			floors_new[key - motion['vel']] = (floors[key][0], floors[key][1])

	return floors_new, floor_needed

##############################################################

def add_floor(floors, floor_needed):
	if floor_needed:
		floors[480] = (randint(90, 160), randint(100, 600))
	return floors

##############################################################

def create_motion():
	motion = {'counter': 25, 'vel': 1.9, 'acc': 0.2}
	return motion

##############################################################

def update_motion(motion):
	if motion['counter'] == 0:
		motion['vel'] = motion['vel'] + motion['acc']
		motion['counter'] = 25
	else:
		motion['counter'] -= 1

	return motion

##############################################################

pg.init()
clock = pg.time.Clock()

# display
dims = 480, 160
screen = pg.display.set_mode(dims)

# game objects
player = create_player()
floors = create_floors()
motion = create_motion()

# game loop
game_status = 1  # 0 for game over, 1 for play
jump_start = 0
jump_time = 0
falling = False
while game_status:

	game_status, jump = process_input()
	
	floors, floor_needed = move_floors(floors, motion)
	floors = add_floor(floors, floor_needed)
	player, jump_start, jump_time, falling = move_player(player, jump, jump_start, jump_time, floors, falling)

	draw_everything(screen, player, floors)
	update_motion(motion)
    
	clock.tick(50)  # or sleep(.02) to have the loop pg-independent