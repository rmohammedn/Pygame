import pygame as pg
import random
import sys

WIDTH = 300
HEIGHT = 400
SPEED = 10
TILESIZE = 10
FPS = 60
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
RATE = 150

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Snack")
        self.clock = pg.time.Clock()
        self.frequency = RATE

    def addSprites(self):
        self.all_sprites = pg.sprite.Group()
        self.snack = pg.sprite.Group()
        self.food = pg.sprite.Group()
        self.player = Snack(self)
        self.cube = Cube(self)

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
        self.player.update()
        self.all_sprites.update()

        #"""
        hits = self.checkCollision()
        if hits:
            print(hits)
            pg.quit()
            sys.exit()
        #"""
        hit = pg.sprite.collide_rect(self.player.head, self.cube)
        if hit:
            self.player.head = self.cube
            self.player.head.image.fill(YELLOW)
            self.player.snack.append(self.player.head)
            #print(len(self.food.sprites()))
            self.cube = Cube(self)
            if self.frequency > 150:
                self.frequency -= 5

    def checkCollision(self):
        size = len(self.player.snack)

        if size < 4:
            return False

        for i in range(size-3):
            hit = pg.sprite.collide_rect(self.player.head, self.player.snack[i])
            if hit:
                return True

        return False



    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        
    def draw(self):
        self.screen.fill(DARKGREY)
        #self.drawGrid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()


class Snack(pg.sprite.Sprite):
    def __init__(self, game):
        self.snack = []
        self.game = game
        self.pos = (WIDTH/2, HEIGHT/2)
        self.head = Cube(self.game)
        self.head.remove(game.food)
        self.head.image.fill(YELLOW)
        self.head.rect.x = WIDTH/2
        self.head.rect.y = HEIGHT/2
        self.snack.append(self.head)
        self.direction = 'right'
        self.last_time = pg.time.get_ticks()

    def update(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.direction != 'down':
                self.direction = 'up'

        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            if self.direction != 'up':
                self.direction = 'down'

        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            if self.direction != 'right':
                self.direction = 'left'

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            if self.direction != 'left':
                self.direction = 'right'

        current_time = pg.time.get_ticks()

        if current_time - self.last_time > game.frequency:
            self.last_time = current_time
            cube = self.snack.pop(0)

            if self.direction == 'up':
                cube.rect.y = (self.head.rect.y - SPEED) % HEIGHT
                cube.rect.x = self.head.rect.x

            elif self.direction == 'down':
                cube.rect.y = (self.head.rect.y + SPEED) % HEIGHT
                cube.rect.x = self.head.rect.x

            elif self.direction == 'left':
                cube.rect.x = (self.head.rect.x - SPEED) % WIDTH
                cube.rect.y = self.head.rect.y

            elif self.direction == 'right':
                cube.rect.x = (self.head.rect.x + SPEED) % WIDTH
                cube.rect.y = self.head.rect.y

            self.head.image.fill(RED)
            self.head = cube
            self.head.image.fill(YELLOW)
            self.snack.append(self.head)





class Cube(pg.sprite.Sprite):

    def __init__(self, game):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH/TILESIZE - 1) * TILESIZE
        self.rect.y = random.randint(0, HEIGHT/TILESIZE - 1) * TILESIZE
        self.type = "cube"


if __name__ == "__main__":
    game = Game()
    game.addSprites()
    game.run()
