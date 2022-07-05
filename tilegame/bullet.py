
import pygame as pg
from settings import *
vector = pg.math.Vector2
IMAGE_PATH = '/home/mohammed/pygame/tilegame/bullet.png'
BULLET_SIZE = (10, 10)
BULLET_SPEED = 500
BULLET_LIFE = 500
BULLET_RATE = 150


class Bullet(pg.sprite.Sprite):
	def __init__(self, game, pos, direction):
		self.group = game.all_sprites, game.bullets
		pg.sprite.Sprite.__init__(self, self.group)
		self.game = game
		self.pos = vector(pos)
		self.dir = direction
		self.loadImage()
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.vel = self.dir * BULLET_SPEED
		self.spawn_time = pg.time.get_ticks()
		self.bullet_rate = BULLET_RATE

	def loadImage(self):
		img = pg.image.load(IMAGE_PATH)
		self.image = pg.transform.scale(img, BULLET_SIZE)

	def update(self):
		self.pos += self.vel * self.game.dt
		self.rect.center = self.pos
		if pg.time.get_ticks() - self.spawn_time > BULLET_LIFE:
			self.kill()
		if pg.sprite.spritecollideany(self, self.game.walls):
			self.kill()





