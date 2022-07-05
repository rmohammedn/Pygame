"""
The Background of any game 

"""

import pygame
import numpy as np

class GridMap(object):
	def __init__(self, width, height):
		self.height = height
		self.width = width
		self.matrix = np.zeros((self.width, self.height))

	def checkGrid(self, width, height):
		rimx = height % self.height
		rimy = width % self.width

		if rimx == 0 and rimy == 0:
			print("tile sizes are correct")
		else:
			print("Grid size should be divisible by tile size")

	def fillRect(self, x1, y1, x2, y2, value=1):
		self.matrix[x1:x2+1, y1, y2+1] = value

	def fillBoundary(self, x1, y1, x2, y2, value=1, thickness=1):
		self.matrix[x1:x1+thickness, y1:y2+1] = value
		self.matrix[x2-thickness+1:x2+1, y1:y2+1] = value
		self.matrix[x1:x2+1, y1:y1+thickness] = value
		self.matrix[x1:x2+1, y2-thickness+1: y2+1] = value

	def drawBorder(self, value=1):
		self.fillBoundary(0, 0, self.width, self.height, value)




class Background(object):

	def __init__ (self, width, height, grid):
		self.height = height
		self.width = width
		self.display = pygame.display.set_mode(width, height)
		self.origin = (0, 0)
		self.gird = grid
		self.max_type = None
		self.grid.checkGrid(width, height)
		self.tile_x = int(self.width / self.grid.width)
		self.tile_y = int(self.height / self.grid.height)

	def setGameName(self, name):
		self.display.set_caption(name)

	def setGameLogo(self, pic, x=32, y=32):
		logo = pygame.image.load(pic)
		scale_logo = pygame.transform(logo, (x, y))
		self.display.set_logo(scale_logo)

	def setImage(self, image, blit_list):
		self.img = pygame.image.load(image)
		self.img1_indx = 0
		self.img2_indx = self.img.get_width()
		#scale_img = pygame.transform(img, (self.width, self.height))
		#self.display.blit(scale_img, self.origin)
		background = (self.img, self.img.get_rect())
		return blit_list

	def createPlatform(self, dict):
		matrix = self.grid.matrix
		self.max_type = np.max(matrix)
		img_dict ={}
		for key, value in dict.items():
			img = pygame.img.load(value)
			scale_img = pygame.transform.scale(img, (self.tile_x, self.tile_y))
			img_dict[key] = scale_img

		self.platform = []
		row_count = 0

		for row in matrix:
			col_count = 0
			for val in row:
				img_rect = img_dict[val].get_rect()
				img_rect.x = col_count * self.tile_x
				img_rect.y = row_count * self.tile_y
				tile = (img_dict[val], img_rect)
				self.platform.append(tile)
				col_count += 1

			row_count += 1

		return blit_list

	def scrollX(self, speed_x):		
		self.img1_indx -= speed_x
		self.img2_indx -= speed_x
		if self.img1_indx <= self.img_width * -1:
			self.img1_indx = self.img_width

		if self.img2_indx <= self.img_width * -1:
			self.img2_indx = self.img_width











if __name__ == "__main__":

	pygame.init()
	height = 800
	width = 1000
	display = pygame.display.set_mode(width, height)
	pygame.display.set_caption("Only Background")