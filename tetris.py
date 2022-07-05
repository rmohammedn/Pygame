import numpy as np
import pygame as pg
import random
import sys

WIDTH = 320
HEIGHT = 640
CENTER = (0, 5)
TILESIZE = 32
SPEED = 5
BLUE = (0, 100, 100)
LIGHTGREY = (100, 100, 100)
DARKGREY = (10, 10, 10)
SPEED = 200

FPS = 60

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Tetris")
        self.clock = pg.time.Clock()
        self.dimension = (HEIGHT//TILESIZE, WIDTH//TILESIZE)
        self.matrix = np.zeros(self.dimension, np.bool)
        self.tile_types = ['T', 'L', 'I', 'Box']
        self.acive_shape = False
        self.all_sprite = pg.sprite.Group()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)

    def getSprite(self):
        self.type = random.choice(self.tile_types)
        self.type = 'I'

        if self.type == 'T':
            shape = Tee(self)

        elif self.type == 'L':
            shape = Ale(self)

        elif self.type == 'I':
            shape = Eye(self)

        elif self.type == 'Box':
            shape = Box(self)

        self.acive_shape = True
        return shape

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)

            #1. check events
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                    self.playing = False
                    pg.quit()
                    sys.exit()

            #2 update the game
            self.update()

            #3 draw the screen
            self.draw()

    def update(self):
        if not self.acive_shape:
            self.shape = self.getSprite()

        self.shape.update()
        if not self.shape.active:
            for i in range(self.shape.number):
                pos = self.shape.pos + self.shape.distance[:, i]
                self.matrix[pos[0, 0], pos[1, 0]] = True

            self.shape.kill()
            self.acive_shape = False

        filled_rows = self.checkRow()
        if len(filled_rows) != 0:
            # do aniimation

            self.matrix = np.delete(self.matrix, filled_rows, axis=0)
            empty_row = np.zeros((len(filled_rows), WIDTH//TILESIZE), np.bool)
            self.matrix = np.vstack((empty_row, self.matrix))

        if self.checkGameOver():
            self.playing = False
            pg.quit()
            sys.exit()

    def checkRow(self):
        filled_rows = []
        indx = 0
        for row in self.matrix:
            if np.all(row):
                filled_rows.append(indx)

            indx += 1

        return filled_rows


    def checkGameOver(self):
        first_row = self.matrix[0]
        if np.any(first_row):
            return True

        return False

    def draw(self):
        self.screen.fill(DARKGREY)
        self.all_sprite.draw(self.screen)
        self.drawGrid()
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self.matrix[row, col]:
                    pos = (col * TILESIZE, row * TILESIZE)
                    self.screen.blit(self.image, pos)

        pg.display.flip()

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    

####============================================= Shape =====================================================#####

class Shape(pg.sprite.Sprite):
    def __init__ (self, game):
        self.game = game
        self.pos = np.matrix(CENTER).reshape((2, 1))
        self.rot_matrix= np.matrix([[0, 1], [-1, 0]])
        self.x_cells = WIDTH//TILESIZE
        self.y_cells = HEIGHT//TILESIZE
        self.last_time = pg.time.get_ticks()
        self.last_loop_time = pg.time.get_ticks()

    def getTiles(self):
        self.tiles = []
        for i in range(self.number):
            tile = Cube(self.game)
            pos = self.pos + self.distance[:, i]
            tile.rect.topleft = (pos[1, 0] * TILESIZE, pos[0, 0] * TILESIZE)
            self.tiles.append(tile)

    def updateCenter(self):
        for i, tile in enumerate(self.tiles):
            center = self.pos + self.distance[:, i]
            tile.rect.topleft = (center[1, 0] * TILESIZE, center[0, 0] * TILESIZE)

    def move(self):
        if not self.active:
            return

        distance = 0
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            current_time = pg.time.get_ticks()
            if current_time - self.last_time > SPEED:
                self.last_time = current_time

                distance = self.rot_matrix.dot(self.distance)
                if not self.checkCollision(distance):
                    self.distance = distance

        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            current_time = pg.time.get_ticks()
            if current_time - self.last_time > SPEED:
                self.last_time = current_time

                self.pos[1, 0] -= 1
                if self.checkCollision():
                    self.pos[1, 0] += 1
            
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            current_time = pg.time.get_ticks()
            if current_time - self.last_time > SPEED:
                self.last_time = current_time

                self.pos[1, 0] += 1
                if self.checkCollision():
                    self.pos[1, 0] -= 1

        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            current_time = pg.time.get_ticks()
            if current_time - self.last_time > SPEED:
                self.last_time = current_time

                while not self.checkCollision():
                    self.pos[0, 0] += 1

                self.pos[0, 0] -= 1

        #"""
        current_time = pg.time.get_ticks()
        if current_time - self.last_loop_time > 500:
            self.last_loop_time = current_time
            self.pos[0, 0] += 1
            if self.checkCollision():
                self.pos[0, 0] -= 1
                self.active = False
        #"""

    def checkCollision(self, distance=[]):
        if len(distance) == 0:
            distance = self.distance
        pos = self.pos

        for i in range(self.number):
            location = self.pos + distance[:, i]
            if location[0, 0] > self.y_cells - 1:
                return True

            if location[1, 0] > self.x_cells - 1 or location[1, 0] < 0:
                return True

            if game.matrix[location[0, 0], location[1, 0]]:
                return True

        return False

    def update(self):
        self.move()
        self.updateCenter()

    def kill(self):
        for tile in self.tiles:
            tile.kill() 


###==================================================== Cube ==================================================###

class Cube(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.group = game.all_sprite
        pg.sprite.Sprite.__init__(self, self.group)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()



###=================================================== TILES ===================================================###

class Tee(Shape):
    def __init__ (self, game):
        super().__init__(game)
        self.number = 4
        self.distance = np.matrix([[0, 0, 0, -1], [0, -1, 1, 0]])
        self.active = True
        self.getTiles()

class Ale(Shape):
    def __init__ (self, game):
        super().__init__(game)
        self.number = 4
        self.distance = np.matrix([[0, -1, 1, 1], [0, 0, 0, 1]])
        self.active = True
        self.getTiles()

class Eye(Shape):
    def __init__ (self, game):
        super().__init__(game)
        self.number = 4
        self.distance = np.matrix([[0, -1, 1, 2], [0, 0, 0, 0]])
        self.active = True
        self.getTiles()

class Box(Shape):
    def __init__ (self, game):
        super().__init__(game)
        self.number = 4
        self.distance = np.matrix([[-1, -1, 0, 0], [-1, 0, -1, 0]])
        self.active = True
        self.getTiles()



if __name__ == "__main__":
    game = Game()
    #game.addSprites()
    game.run()
