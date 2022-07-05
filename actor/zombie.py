
import pygame as pg
from settings import *
vector = pg.math.Vector2
MOB_SPEED = 50
HIT_RECT_WIDTH = 32
HIT_RECT_HEIGHT = 32
IMAGE_PATH = "/home/mohammed/pygame/actor/images/shooter/zombie1_hold.png"

class Zombie(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.base_image = pg.image.load(IMAGE_PATH)
		self.rect = self.image.get_rect()
		self.pos = pg.math.Vector2(x, y) * TILESIZE
		self.vel = pg.math.Vector2(0, 0)
		self.acc = pg.math.Vector2(0, 0)
		self.hit_rect = pg.Rect(0, 0, HIT_RECT_WIDTH, HIT_RECT_HEIGHT)
		self.angle = 0
		self.hit_rect.center = self.rect.center
		self.name = "Zombie mob"

	def update(self):
		self.angle = (self.game.player.pos - self.pos).angle_to(vector(1, 0))
		self.image = pg.transform.rotate(self.base_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.acc = vector(MOB_SPEED, 0).rotate(-self.angle)
		self.acc += self.vel * -1
		self.vel += self.acc * self.game.dt
		self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt**2
		self.hit_rect.centerx = self.pos.x
		self.checkCollision('x')
		self.hit_rect.centery = self.pos.y
		self.checkCollision('y')
		self.rect.center = self.hit_rect.center

	def checkCollision(self, dir):
		if (dir == 'x'):
			hits = pg.sprite.spritecollide(self, self.game.walls, False, self.collisionHitBox)
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
