
import pygame as pg
from settings import *


class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.name = "Wall"
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
