

import pygame

walk_right = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), \
             pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), \
             pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walk_left = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), \
            pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), \
            pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
bg = pygame.image.load('images/bg.jpg')
bgx = 0
bgx2 = bg.get_width()

char = pygame.image.load('images/standing.png')

class Player(object):
	def __init__(self, x, y, width, hight):
		self.x = x
		self.y = y
		self.width = width
		self.hight = hight
		self.speed = 5
		self.left = False
		self.right = False
		self.step_count = 0
		self.jump_hight = 10
		self.jump = False
		self.player_form = 27

	def draw(self, win):
		self.step_count = (self.step_count) % 27
		if self.left:
			win.blit(walk_left[self.step_count // 3], (self.x, self.y))
			self.step_count += 1

		elif self.right:
			win.blit(walk_right[self.step_count //3], (self.x, self.y))
			self.step_count += 1
		else:
			win.blit(char, (self.x, self.y))
			self.step_count


class Display(object):
	def __init__(self, width, hight):
		self.width = width
		self.hight = hight
		self.win = pygame.display.set_mode((self.width, self.hight))

	def reDrawWin(self, player):
		self.win.blit(bg, (bgx,0))
		self.win.blit(bg, (bgx2, 0))
		player.draw(self.win)
		pygame.display.update()


def main():

	pygame.init()
	win = Display(500, 500)
	man = Player(200, 410, 64, 64)
	clock = pygame.time.Clock()
	global bgx, bgx2

	run = True
	while run:
		clock.tick(27)

		bgx -= 2
		bgx2 -= 2
		if bgx < bg.get_width() * -1:
			bgx = bg.get_width()

		if bgx2 < bg.get_width() * -1:
			bgx2 = bg.get_width()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] and man.x > man.speed:
			man.left = True
			man.x -= man.speed
			man.right = False

		elif keys[pygame.K_RIGHT] and man.x < win.width - man.width - man.speed:
			man.right = True
			man.x += man.speed
			man.left = False

		else:
			man.step_count = 0
			man.right = False
			man.left = False

		if not man.jump:
			if keys[pygame.K_UP]:
				man.jump = True
				man.right = False
				man.left = False
				man.step_count = 0

		else:
			if man.jump_hight >= -10:
				direction = 1
				if man.jump_hight < 0:
					direction = -1

				man.y -= round((man.jump_hight ** 2) * 0.5 * direction)
				man.jump_hight -= 1

			else:
				man.jump = False
				man.jump_hight = 10

		win.reDrawWin(man)


if __name__ == "__main__":

	main()




