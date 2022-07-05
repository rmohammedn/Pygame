

import pygame as pg
from settings import *
#vec = pg.math.Vector2

PLAYER_SPEED = 200
PLAYER_ANGULAR_SPEED = 250
HIT_RECT_WIDTH = 36
HIT_RECT_HEIGHT = 36
IMAGE_PATH = "/home/mohammed/pygame/actor/images/shooter/manBlue.png"
IMAGE_SIZE = (30, 30)

def collisionHitBox(spr1, spr2):
		return spr1.hit_rect.colliderect(spr2.rect)

class Shooter(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.name = "Shooter"
		self.getImage()
		self.rect = self.image.get_rect()
		self.pos = pg.math.Vector2(x, y) * TILESIZE
		self.vel = pg.math.Vector2(0, 0)
		self.hit_rect = pg.Rect(0, 0, HIT_RECT_WIDTH, HIT_RECT_HEIGHT)
		self.hit_rect.center = self.rect.center
		self.angle = 0

	def getImage(self):
		self.base_image = self.image = pg.image.load(IMAGE_PATH)
		#self.image = self.base_image

	def move(self):
		self.rotation_speed = 0
		self.vel.x = 0
		self.vel.y = 0
		keys = pg.key.get_pressed()
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.rotation_speed = PLAYER_ANGULAR_SPEED

		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.rotation_speed = -PLAYER_ANGULAR_SPEED

		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel = pg.math.Vector2(PLAYER_SPEED, 0).rotate(-self.angle)

		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel = pg.math.Vector2(-PLAYER_SPEED/2.0, 0).rotate(-self.angle)

	def checkCollision(self, dir):
		if (dir == 'x'):
			hits = pg.sprite.spritecollide(self, self.game.walls, False, collisionHitBox)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - HIT_RECT_WIDTH/2

				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right + HIT_RECT_WIDTH/2

				self.vel.x = 0
				self.hit_rect.centerx = self.pos.x

		if (dir == 'y'):
			hits = pg.sprite.spritecollide(self, self.game.walls, False, self.collisionHitBox)
			if hits:
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - HIT_RECT_HEIGHT/2

				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom + HIT_RECT_HEIGHT/2

				self.vel.y = 0
				self.hit_rect.centery = self.pos.y

	def collisionHitBox(self, spr1, spr2):
		return spr1.hit_rect.colliderect(spr2.rect)


	def update(self):
		self.move()
		self.angle = (self.angle + self.rotation_speed * self.game.dt) % 360
		self.image = pg.transform.rotate(self.base_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.pos += self.vel * self.game.dt
		self.hit_rect.centerx = self.pos.x
		self.checkCollision('x')
		self.hit_rect.centery = self.pos.y
		self.checkCollision('y')
		self.rect.center = self.pos
