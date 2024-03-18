import pygame as pg, sys
from helper.myconstants import *
from helper.scene import Scene
from helper.events import EventHandler

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.running = True
        self.scene = Scene(self)
    
    def run(self):
        while self.running:
            self.update()
            self.draw()
        self.close()

    def update(self):
        EventHandler.poll_events()
        for e in EventHandler.events:
            if e.type == pg.QUIT:
                self.running = False

        self.scene.update()
        pg.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.scene.draw()

    def close(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()