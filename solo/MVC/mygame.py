# BY SAHAND NAYEBAZIZ
# UCI SPRING 2014
#
# mvc structure adapted from T. Debeauvais INF 123 class material

from random import randint
import pygame as pg
from network import Handler, poll

class Model():
	def __init__(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 600)} # the key is the x-coord, value[0] is the y-coord, and value[1] is the width
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'menu', 'multi_status': 'init', 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': 0, 'high_score': 0, 'current_score': 0} # "dashboard" containing all stats
	def reset_menu(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 600)}
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'menu', 'multi_status': self.dash['multi_status'], 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': self.dash['menu_selection'], 'high_score': self.dash['high_score'], 'current_score': 0} # "dashboard" containing all stats
	def reset_single(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 900)}
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'single', 'multi_status': self.dash['multi_status'], 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': 0, 'high_score': self.dash['high_score'], 'current_score': 0} # "dashboard" containing all stats
	def reset_multi(self):
		self.player = {'x': 60, 'y': 30, 'width': 7, 'height': 30}
		self.floors = {0: (120, 900)}
		self.motion = {'counter': 25, 'vel': 3, 'acc': 0.3}
		self.dash = {'game_status': 'multi', 'multi_status': self.dash['multi_status'], 'multi_timer': 0, 'multi_countdown': 750, 'rdy': 0, 'jumping': False, 'jump_start': 0,  'jump_time': 0, 'falling': False, 'frames_traveled': 0, 'menu_selection': 0, 'high_score': self.dash['high_score'], 'current_score': 0} # "dashboard" containing all stats
		self.color = (255, 255, 255)
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
			    screen.blit(title, (230, 30))
			    subfont = pg.font.Font('range.ttf', 20)
			    subtitle = subfont.render('HIGH SCORE', 50, (100, 100, 100))
			    screen.blit(subtitle, (180, 70))
		if self.m.dash['frames_traveled'] >= 150:
			if pg.font:
				font = pg.font.Font('range.ttf', 12)
				score = font.render("score: " + str(self.m.dash['current_score']), 50, (80, 80, 80))
				screen.blit(score, (420, 10))
		pg.display.update()
		self.m.dash['frames_traveled'] += 1
		self.m.dash['current_score'] = (self.m.dash['frames_traveled'] - 100) / 150

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
		    if self.m.dash['high_score'] != 0:
		    	score = little_font.render(("your best run... " + str(self.m.dash['high_score'])), 1, (90,90,90))
		    	screen.blit(score, (353, 100))
		pg.display.update()

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
				    screen.blit(title, (230, 30))
				    subfont = pg.font.Font('range.ttf', 20)
				    subtitle = subfont.render('HIGH SCORE!', 50, (100, 100, 100))
				    screen.blit(subtitle, (175, 70))
			else:
				if pg.font:
				    font = pg.font.Font('range.ttf', 40)
				    title = font.render(str(self.m.dash['high_score']), 50, (255, 255, 255))
				    screen.blit(title, (230, 30))
				    subfont = pg.font.Font('range.ttf', 20)
				    subtitle = subfont.render('Meh.', 50, (100,100,100))
				    screen.blit(subtitle, (220, 70))
			pg.display.update()
			self.m.dash['frames_traveled'] += 1

	def display_multi(self):
		if self.m.dash['multi_status'] == 'connected':
			network_message = 'Now connected to the server!'
		else:
			network_message = 'Uh-oh... no server connection :('
		
		if self.m.dash['multi_status'] == 'connected':
			if self.m.dash['multi_timer'] >= 0 and self.m.dash['multi_timer'] < 100:
				screen = self.screen
				screen.fill((32, 32, 32))
				font = pg.font.Font('range.ttf', 19)
				message = font.render(network_message, 1, (255, 255, 255))
				screen.blit(message, (96, 66))
				pg.display.update()
				self.m.dash['multi_timer'] += 1
			else:
				self.m.dash['multi_timer'] = 0
				self.m.dash['multi_status'] = 'ready'



		if self.m.dash['multi_status'] == 'ready':
			if self.m.dash['multi_countdown'] >= 0:
				# am I dead?
				if self.m.player['x'] + self.m.player['width'] < 0 or self.m.player['y'] > self.dims['y']:
					self.m.reset_menu()
				if self.m.player['y'] < 30:
					self.camera['y'] = self.m.player['y'] - 30
				screen = self.screen
				screen.fill((32, 32, 32))
				all_colors = [(255, 0, 0),(255, 127, 0), (255, 255, 0), (100, 150, 100), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
				pg.draw.rect(screen, all_colors[randint(0,6)], (self.m.player['x'], self.m.player['y'] - self.camera['y'], self.m.player['width'], self.m.player['height']))
				for x in range(1, (self.m.dash['rdy'])):
					pg.draw.rect(screen, (100, 100, 100), (((self.m.player['x'] + self.m.player['width'] + (x * self.m.player['width'])) + ((x - 1) * self.m.player['width'])), 90, self.m.player['width'], self.m.player['height']))
				for key in self.m.floors:
					pg.draw.rect(screen, (50, 50, 50), (key, self.m.floors[key][0] - self.camera['y'], self.m.floors[key][1], 600))
				if self.m.dash['menu_selection'] == 0:
					colors = ((102, 202, 204), (120, 120, 120))
				else:
					colors = ((120, 120, 120), (102, 202, 204))
				if pg.font:
				    big_font = pg.font.Font('range.ttf', 19)
				    little_font = pg.font.Font('range.ttf', 12)
				    title = big_font.render("New game starting in... " + (str(self.m.dash['multi_countdown'] / 50)), 1, (255, 255, 255))
				    screen.blit(title, (96, 30))
				    if self.m.dash['high_score'] != 0:
				    	score = little_font.render(("your best run... " + str(self.m.dash['high_score'])), 1, (90,90,90))
				    	screen.blit(score, (353, 100))
				pg.display.update()
				self.m.dash['multi_countdown'] -= 1
			if self.m.dash['multi_countdown'] < 0:
				self.m.dash['multi_status'] = 'starting'
				self.m.dash['multi_timer'] = 0

		if self.m.dash['multi_status'] == 'starting':
			if self.m.dash['multi_timer'] >= 0 and self.m.dash['multi_timer'] < 500:
				screen = self.screen
				screen.fill((32, 32, 32))
				font = pg.font.Font('range.ttf', 19)
				message = font.render("and...................", 1, (255, 255, 255))
				screen.blit(message, (96, 66))
				pg.display.update()
				self.m.dash['multi_timer'] += 1
			else:
				self.m.dash['multi_timer'] = 0
				self.m.dash['multi_status'] = 'menu'


		
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
					self.m.dash['game_status'] = 'multi'
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

		elif self.m.dash['game_status'] == 'multi':
			if self.m.dash['multi_status'] == 'connected':
				for event in pg.event.get():
					if event.type == pg.QUIT:
						self.m.dash['game_status'] = 0
				key = pg.key.get_pressed()
				if key[pg.K_BACKSPACE]:
					self.m.dash['game_status'] = 'menu'
			if self.m.dash['multi_status'] == 'ready':
				self.m.dash['jumping'] = 0
				for event in pg.event.get():
					if event.type == pg.QUIT:
						self.m.dash['game_status'] = 0 # 0 for game over, 1 for play
				key = pg.key.get_pressed()
				if key[pg.K_UP] or key[pg.K_SPACE]:
					self.m.dash['jumping'] = 1
				elif key[pg.K_BACKSPACE]:
					self.m.dash['game_status'] = 'menu'
			if self.m.dash['multi_status'] == 'starting':
				for event in pg.event.get():
					if event.type == pg.QUIT:
						self.m.dash['game_status'] = 0 # 0 for game over, 1 for play
				key = pg.key.get_pressed()
				if key[pg.K_BACKSPACE]:
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

class MyHandler(Handler):
    
    def __init__(self, m):
    	self.m = m
        host, port = 'localhost', 8899
        Handler.__init__(self, host, port)
        
    def on_close(self):
        pass
        
    def on_msg(self, msg):
    	if 'news' in msg:
    		if msg['news'] == 'connected':
    			print('all satisfied')
    			self.m.dash['multi_status'] = 'connected'
    	if 'num_rdy' in msg:
    		self.m.dash['rdy'] = msg['num_rdy']
            
    def send_msg(self, txt):
        self.do_send({'txt': txt})
        
    def update(self):
        poll(0.01)
        
    def kill(self):
        self.close()  # will call on_close

############# LOOP #############
pg.init()
pg.font.init()
model = Model()
c = Controller(model)
n = MyHandler(model) # handler will be initialized here
v = View(model)
clock = pg.time.Clock()

while model.dash['game_status']:
	while model.dash['game_status'] == 'menu':
		c.process_input()
		c.move_floors()
		c.move_player()
		v.display_menu()
		c.turn_world()
		n.update()
		clock.tick(50)
	if model.dash['game_status'] == 'single':
		model.reset_single()
		while model.dash['game_status'] == 'single':
			c.process_input()
			c.move_floors()
			c.move_player()
			v.display()
			c.turn_world()
			clock.tick(50)
		if model.dash['game_status'] == 'menu':
			model.reset_menu()
	if model.dash['game_status'] == 'multi':
		model.reset_multi()
		while model.dash['game_status'] == 'multi':
			if model.dash['multi_status'] == 'connected':
				c.process_input()
				v.display_multi()
				n.update()	
				clock.tick(50)
			elif model.dash['multi_status'] == 'ready':
				c.process_input()
				c.move_player()
				v.display_multi()
				n.update()
				n.send_msg('rdy')
				clock.tick(50)
				print(model.dash['rdy'])
			elif model.dash['multi_status'] == 'starting':
				c.process_input()
				c.move_player()
				v.display_multi()
				n.update()
				n.send_msg('lesgo')
				clock.tick(50)
		if model.dash['game_status'] == 'menu':
			model.reset_menu()



