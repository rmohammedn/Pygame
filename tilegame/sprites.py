
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.getImage()
		self.game = game
		self.rect = self.image.get_rect()
		self.vx = 0
		self.vy = 0
		self.gridx = x
		self.gridy = y
		self.x = x * TILESIZE
		self.y = y * TILESIZE

	def getImage(self):
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(YELLOW)

	def move(self):
		self.vx, self.vy = 0, 0
		key = pg.key.get_pressed()
		if key[pg.K_LEFT] or key[pg.K_a]:
			self.vx = -PLAYER_SPEED

		if key[pg.K_RIGHT] or key[pg.K_d]:
			self.vx = PLAYER_SPEED

		if key[pg.K_UP] or key[pg.K_w]:
			self.vy = -PLAYER_SPEED

		if key[pg.K_DOWN] or key[pg.K_s]:
			self.vy = PLAYER_SPEED

		if self.vx != 0 and self.vy != 0:
			self.vx *= 0.7071
			self.vy *= 0.7071

	def checkCollision(self, dir):
		if dir == 'x':
			hits = pg.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				if self.vx > 0:
					self.x = hits[0].rect.left - self.rect.width

				if self.vx < 0:
					self.x = hits[0].rect.right

				self.vx = 0
				self.rect.x = self.x

		if dir == 'y':
			hits = pg.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				if self.vy > 0:
					self.y = hits[0].rect.top - self.rect.height

				if self.vy < 0:
					self.y = hits[0].rect.bottom

				self.vy = 0
				self.rect.y = self.y

	def update(self):
		self.move()
		self.x += self.vx * self.game.dt
		self.y += self.vy * self.game.dt
		self.rect.x = self.x
		self.checkCollision('x')
		self.rect.y = self.y
		self.checkCollision('y')


"""
class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.getImage()
		self.rect = self.image.get_rect()
		self.gridx = x
		self.gridy = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

	def getImage(self):
		#self.image = pg.Surface((TILESIZE, TILESIZE))
		#self.image.fill(GREEN)
		self.image = pg.transform.scale(pg.image.load("tile.png"), (TILESIZE, TILESIZE))



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
"""