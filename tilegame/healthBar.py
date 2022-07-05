
import pygame as pg

class HealthBar:
	red = (255, 0, 0)
	green = (0, 255, 0)
	yellow = (255, 255, 0)

	def __init__(self, max_health, width=15, thickness=5):
		self.max_health = max_health
		self.width = width
		self.thickness = thickness

	def update(self, health, image):
		if health > 0.6 * self.max_health:
			color = self.green
		elif health > 0.3 * self.max_health and health < 0.7 * self.max_health:
			color = self.yellow
		else:
			color = self.red

		width = int(self.width * health / self.max_health)
		health_bar = pg.Rect(0, 0, width, self.thickness)
		if health <= self.max_health:
			pg.draw.rect(image, color, health_bar)







