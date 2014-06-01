# BY SAHAND NAYEBAZIZ
# UCI SPRING 2014
#
# mvc structure adapted from T. Debeauvais INF 123 class material

from random import randint
import pygame as pg

class Model():
	def __init__(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 600)} # the key is the x-coord, value[0] is the y-coord, and value[1] is the width
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'menu', 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': 0, 'high_score': 0, 'current_score': 0} # "dashboard" containing all stats
	def reset_menu(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 600)}
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'menu', 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': self.dash['menu_selection'], 'high_score': self.dash['high_score'], 'current_score': 0} # "dashboard" containing all stats
	def reset_playing(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 900)}
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'single', 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': 0, 'high_score': self.dash['high_score'], 'current_score': 0} # "dashboard" containing all stats

class View():
	def __init__(self, model):
		self.m = model
		self.dims = {'x': 480, 'y': 160}
		self.camera = {'y': 0}
		self.screen = pg.display.set_mode((self.dims['x'], self.dims['y']))

	def display(self):
		# am I dead?
		if self.m.player['x'] + self.m.player['width'] < 0 or self.m.player['y'] > self.dims['y']:
			self.freeze()
			self.m.dash['game_status'] = 'menu'
		if self.m.player['y'] < 30:
			self.camera['y'] = self.m.player['y'] - 30
		screen = self.screen
		screen.fill((32, 32, 32))
		pg.draw.rect(screen, (255, 255, 255), (self.m.player['x'], self.m.player['y'] - self.camera['y'], self.m.player['width'], self.m.player['height']))
		for key in self.m.floors:
			pg.draw.rect(screen, (90, 90, 90), (key, self.m.floors[key][0] - self.camera['y'], self.m.floors[key][1], 600))
		
		if self.m.dash['frames_traveled'] > 20 and self.m.dash['frames_traveled'] < 190:
			if pg.font:

			    font = pg.font.Font('range.ttf', 40)
			    title = font.render(str(self.m.dash['high_score']), 50, (255, 255, 255))
			    screen.blit(title, (220, 30))
			    subfont = pg.font.Font('range.ttf', 20)
			    subtitle = subfont.render('HIGH SCORE', 50, (100, 100, 100))
			    screen.blit(subtitle, (165, 70))

		if self.m.dash['frames_traveled'] >= 150:
			if pg.font:
				font = pg.font.Font('range.ttf', 12)
				score = font.render("score: " + str(self.m.dash['current_score']), 50, (80, 80, 80))
				screen.blit(score, (420, 10))

		pg.display.update()
		self.m.dash['frames_traveled'] += 1
		self.m.dash['current_score'] = (self.m.dash['frames_traveled'] - 100) / 150

	def freeze(self):
		screen = self.screen
		current_time = self.m.dash['frames_traveled']
		high_score = self.m.dash['current_score'] > self.m.dash['high_score']
		while self.m.dash['frames_traveled'] - current_time < 190:
			screen.fill((32, 32, 32))
			for key in self.m.floors:
				pg.draw.rect(screen, (50, 50, 50), (key, self.m.floors[key][0] - self.camera['y'], self.m.floors[key][1], 600))
			if high_score:
				self.m.dash['high_score'] = self.m.dash['current_score']
				if pg.font:
				    font = pg.font.Font('range.ttf', 40)
				    title = font.render(str(self.m.dash['high_score']), 50, (255, 255, 255))
				    screen.blit(title, (220, 30))
				    subfont = pg.font.Font('range.ttf', 20)
				    subtitle = subfont.render('HIGH SCORE!!!', 50, (100, 100, 100))
				    screen.blit(subtitle, (165, 70))
			else:
				if pg.font:
				    font = pg.font.Font('range.ttf', 40)
				    title = font.render(str(self.m.dash['high_score']), 50, (255, 255, 255))
				    screen.blit(title, (220, 30))
				    subfont = pg.font.Font('range.ttf', 20)
				    subtitle = subfont.render('Meh.', 50, (100,100,100))
				    screen.blit(subtitle, (210, 70))
			pg.display.update()
			self.m.dash['frames_traveled'] += 1

	def display_menu(self):
		# am I dead?
		if self.m.player['x'] + self.m.player['width'] < 0 or self.m.player['y'] > self.dims['y']:
			self.m.reset_menu()
		if self.m.player['y'] < 30:
			self.camera['y'] = self.m.player['y'] - 30
		screen = self.screen
		screen.fill((32, 32, 32))
		pg.draw.rect(screen, (100, 100, 100), (self.m.player['x'], self.m.player['y'] - self.camera['y'], self.m.player['width'], self.m.player['height']))
		for key in self.m.floors:
			pg.draw.rect(screen, (50, 50, 50), (key, self.m.floors[key][0] - self.camera['y'], self.m.floors[key][1], 600))
		if self.m.dash['menu_selection'] == 0:
			colors = ((102, 202, 204), (120, 120, 120))
		else:
			colors = ((120, 120, 120), (102, 202, 204))
		
		

		if pg.font:
		    big_font = pg.font.Font('range.ttf', 26)
		    little_font = pg.font.Font('range.ttf', 12)

		    title = big_font.render("Cave Run.", 1, (255, 255, 255))
		    play = little_font.render("run alone", 1, colors[0])   
		    quit = little_font.render("run with friends", 1, colors[1])

		    screen.blit(title, (330, 40))
		    screen.blit(play, (280, 75))
		    screen.blit(quit, (355, 75))

		pg.display.update()

class Controller():

	def __init__(self, m):
		self.m = m
		pg.init()

	def process_input(self):

		if self.m.dash['game_status'] == 'menu':
			self.m.dash['jumping'] = 0
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.m.dash['game_status'] = 0 # 0 for game over, 1 for play
			key = pg.key.get_pressed()
			if key[pg.K_UP] or key[pg.K_SPACE]:
				self.m.dash['jumping'] = 1
			elif key[pg.K_RIGHT]:
				self.m.dash['menu_selection'] = 1
			elif key[pg.K_LEFT]:
				self.m.dash['menu_selection'] = 0
			elif key[pg.K_ESCAPE]:
				self.m.dash['game_status'] = 0
			elif key[pg.K_RETURN]:
				if self.m.dash['menu_selection'] == 1:
					self.m.dash['game_status'] = 0
				if self.m.dash['menu_selection'] == 0:
					self.m.dash['game_status'] = 'single'

		elif self.m.dash['game_status'] == 'single':
			self.m.dash['jumping'] = 0
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.m.dash['game_status'] = 0
			key = pg.key.get_pressed()
			if key[pg.K_UP] or key[pg.K_SPACE]:
				self.m.dash['jumping'] = 1
			elif key[pg.K_BACKSPACE]:
				self.m.dash['game_status'] = 'menu'

	def move_player(self):
		if self.m.dash['falling']:
			self.m.dash['jumping'] = False
		if not self.m.dash['jumping']:
			self.m.dash['falling'] = True
			self.m.dash['jump_start'], self.m.dash['jump_time'] = 0, 0
			self.m.player['y'] += 4
		if not self.m.dash['falling']:
			if self.m.dash['jumping']:
				if self.m.dash['jump_time'] == 0:
					self.m.dash['jump_start'] = pg.time.get_ticks() + 1
					self.m.player['y'] -= 10
					self.m.dash['jump_time'] = 1
				elif self.m.dash['jump_time'] <= 50:
					self.m.player['y'] -= 7.7
					self.m.dash['jump_time'] = pg.time.get_ticks() - self.m.dash['jump_start']
				elif self.m.dash['jump_time'] < 100:
					self.m.player['y'] -= 5.2
					self.m.dash['jump_time'] = pg.time.get_ticks() - self.m.dash['jump_start']
				elif self.m.dash['jump_time'] < 200:
					self.m.player['y'] -= 3.0
					self.m.dash['jump_time'] = pg.time.get_ticks() - self.m.dash['jump_start']
				elif self.m.dash['jump_time'] < 260:
					self.m.player['y'] -= 0.9
					self.m.dash['jump_time'] = pg.time.get_ticks() - self.m.dash['jump_start']
				elif self.m.dash['jump_time'] >= 260:
					self.m.dash['falling'] = True
		for key in self.m.floors:
			colliding = pg.Rect(key, self.m.floors[key][0], self.m.floors[key][1], 600).colliderect(pg.Rect(self.m.player['x'], self.m.player['y'], self.m.player['width'], self.m.player['height']))
			if colliding:
				if self.m.player['x'] > key:
					self.m.dash['falling'] = False
				if self.m.player['x'] > key and self.m.player['y'] + (self.m.player['height']/4) < self.m.floors[key][0]:
					self.m.player['y'] = self.m.floors[key][0] - self.m.player['height']
				elif (self.m.player['y'] + self.m.player['height']) >= self.m.floors[key][0]:
					self.m.player['x'] = key - self.m.player['width']
					self.m.dash['falling'] = True

	def move_floors(self):
		needing_floor = True
		if len(self.m.floors) != 0:
			for key in self.m.floors:
				if (key + self.m.floors[key][1] > randint(339, 460)):
					needing_floor = False
			floors_new = {}
			for key in self.m.floors:
				floors_new[key - self.m.motion['vel']] = (self.m.floors[key][0], self.m.floors[key][1])
			self.m.floors = floors_new
		if needing_floor:
			self.m.floors[480] = (randint(90, 154), randint(100, 800))
			self.m.dash['frames_traveled'] += 50

	def turn_world(self):
		if self.m.motion['counter'] == 0:
			self.m.motion['vel'] = self.m.motion['vel'] + self.m.motion['acc']
			self.m.motion['counter'] = 25
		else:
			self.m.motion['counter'] -= 1

############# LOOP #############
pg.init()
pg.font.init()
model = Model()
c = Controller(model)
v = View(model)
clock = pg.time.Clock()

while model.dash['game_status']:
	while model.dash['game_status'] == 'menu':
		c.process_input()
		c.move_floors()
		c.move_player()
		v.display_menu()
		c.turn_world()
		clock.tick(50)
	if model.dash['game_status']:
		model.reset_playing()
	while model.dash['game_status'] == 'single':
		c.process_input()
		c.move_floors()
		c.move_player()
		v.display()
		c.turn_world()
		clock.tick(50)
	if model.dash['game_status']:
		model.reset_menu()
