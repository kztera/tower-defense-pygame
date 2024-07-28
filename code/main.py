import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH_DEFAULT, SCREEN_HEIGHT_DEFAULT), pygame.RESIZABLE
        )
        pygame.display.set_caption("Tower Defense PyGame")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    # Update the window size when the player resizes it
                    # window_width, window_height = event.size
                    # self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                    print("event.size")

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
