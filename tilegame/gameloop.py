
import pygame as pg
#from sprites import *
from shooter import *
#from check import *
from walls import *
from settings import *
from camera import *
from zombie import *
import os
import sys

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()

    def loadData(self):
        directory = os.path.dirname(__file__)
        self.map = Map(os.path.join(directory, "maze.txt"))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)

                if tile == 'P':
                    self.player = Shooter(self, col, row)

                if tile == 'M':
                    self.zombie = Zombie(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(DARKGREY)
        self.drawGrid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.K_ESCAPE:
                self.quit()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.zombies, False, collisionHitBox)
        for hit in hits:
            self.player.health -= 10
        hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
        for hit in hits:
            hit.health -= 10

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()

    while True:
        game.new()
        game.run()

