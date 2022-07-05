
import pygame as pg
from settings import *
PLAYER_SPEED = 5
JUMP_LIMIT = 10

class Hero(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self.groups)
		self.game = game
		self.gridx = x
		self.gridy = y
		self.pixal_x = x * TILESIZE
		self.pixal_y = y * TILESIZE
		self.image_frame = 0
		self.jump = False
		self.jump_height = JUMP_LIMIT
		self.direction = 0 		# {left: -1, front: 0, right: 1}
		self.image_path = "/home/mohammed/pygame/actor/images/hero/"
		self.loadImages()

	def loadImages(self):
		self.walk_right = [pygame.image.load(self.image_path + 'R1.png'), pygame.image.load(self.image_path + 'R2.png'), \
						   pygame.image.load(self.image_path + 'R3.png'), pygame.image.load(self.image_path + 'R6.png'), \
             			   pygame.image.load(self.image_path + 'R7.png'), pygame.image.load(self.image_path + 'R8.png'), \
             			   pygame.image.load(self.image_path + 'R9.png')]
		self.walk_left = [pygame.image.load(self.image_path + 'L1.png'), pygame.image.load(self.image_path + 'L2.png'), \
						  pygame.image.load(self.image_path + 'L3.png'), pygame.image.load(self.image_path + 'L4.png'), \
						  pygame.image.load(self.image_path + 'L5.png'), pygame.image.load(self.image_path + 'L6.png'), \
            			  pygame.image.load(self.image_path + 'L7.png'), pygame.image.load(self.image_path + 'L8.png'), \
            			  pygame.image.load(self.image_path + 'L9.png')]
		self.stand = pygame.image.load(self.image_path + 'standing.png')

	def move(self):
		key = pg.key.get_pressed()

		if keys[pg.K_LEFT] or key[pg.K_a]:
			self.pixal_x -= PLAYER_SPEED
			self.direction = -1

		elif key[pg.K_RIGHT] or key[pg.K_d]:
			self.pixal_x += PLAYER_SPEED
			self.direction = 1

		else:
			self.direction = 0


		if not self.jump:
			if key[pg.K_UP] or key[pg.K_w]:
				self.jump = True

		else:
			self.checkCollision()
			if self.jump_height > -JUMP_LIMIT:
				if self.jump_hight < 0:
					up = -1
				else:
					up = 1

				self.pixal_y -= round((self.jump_hight ** 2) * 0.5 * up)
				self.jump_hight -= 1

			else:
				self.jump = False
				self.jump_hight = 10

	def checkCollision(self):


	def update(self):
		self.move()
		self.image_frame %= 27

		if self.direction = 1:
			self.image = self.walk_right[int(self.image_frame / 3)]
			self.image_frame += 1
			self.rect = self.image.get_rect()

		elif self.direction = -1:
			self.image = self.walk_left[int(self.image_frame / 3)]
			self.image_frame += 1
			self.rect = self.image.get_rect()

		else:
			self.image = self.stand
			self.rect = self.image.get_rect()

		self.checkCollision('x')
		self.checkCollision('y')

