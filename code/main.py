import pygame, sys
from settings import *
from level import Level
from asset_path import *
from game_stats import *
import random


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH_DEFAULT, SCREEN_HEIGHT_DEFAULT), pygame.RESIZABLE
        )
        pygame.display.set_caption("Tower Defense PyGame")
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Create a surface for day/night cycle
        self.day_night_surface = pygame.Surface(
            (SCREEN_WIDTH_DEFAULT, SCREEN_HEIGHT_DEFAULT)
        )
        self.day_night_surface.set_alpha(0)
        self.day_length = 75
        self.night_length = 75
        self.intersection_length = 15
        self.time_elapsed = 0

        self.font_text = pygame.font.Font((ASSET_PATH_FONT + FONT_TEXT + ".ttf"), 36)

        self.day_music = [f"{ASSET_MUSIC_DAY}{i}.mp3" for i in range(1, 163)]
        self.night_music = [f"{ASSET_MUSIC_NIGHT}{i}.mp3" for i in range(1, 58)]

        self.current_music = None
        self.is_day = True
        self.fade_time = 2000

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)

        self.play_random_music(self.is_day)

    def play_random_music(self, is_day):
        if is_day:
            new_music = random.choice(self.day_music)
        else:
            new_music = random.choice(self.night_music)

        if new_music != self.current_music:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(self.fade_time)
                pygame.time.wait(self.fade_time)  # Đợi cho nhạc cũ fade out

            pygame.mixer.music.load(new_music)
            pygame.mixer.music.play(fade_ms=self.fade_time)
            self.current_music = new_music

    def update_day_night_cycle(self, dt):
        self.time_elapsed += dt
        cycle_length = self.day_length + self.night_length
        current_time = self.time_elapsed % cycle_length

        if current_time < self.day_length:
            # Day time
            if not self.is_day:
                self.is_day = True
                self.play_random_music(True)

            if current_time >= self.day_length - self.intersection_length:
                progress = (
                    current_time - (self.day_length - self.intersection_length)
                ) / self.intersection_length
                alpha = int(150 * progress)
                self.day_night_surface.set_alpha(alpha)

                text = self.font_text.render("Night is coming", True, (255, 255, 255))
                text.set_alpha(255 - int(255 * progress))
                text_rect = text.get_rect(
                    center=(SCREEN_WIDTH_DEFAULT // 2, SCREEN_HEIGHT_DEFAULT // 4)
                )
                self.screen.blit(text, text_rect)
            else:
                self.day_night_surface.set_alpha(0)
        else:
            # Night time
            if self.is_day:
                self.is_day = False
                self.play_random_music(False)

            if current_time >= cycle_length - self.intersection_length:
                progress = (
                    current_time - (cycle_length - self.intersection_length)
                ) / self.intersection_length
                alpha = int(150 * (1 - progress))
                self.day_night_surface.set_alpha(alpha)
            else:
                self.day_night_surface.set_alpha(150)

        # Apply the day/night surface to the screen
        self.screen.blit(self.day_night_surface, (0, 0))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            self.update_day_night_cycle(dt)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
