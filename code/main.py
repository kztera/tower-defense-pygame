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

        self.display_surface = pygame.display.get_surface()

        # sound
        self.default_volume = 0.1
        self.current_volume = self.default_volume
        self.time_bar_x = self.display_surface.get_width() - 100

        # time
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.night_count = 0

        # Create a surface for day/night cycle
        self.day_night_surface = pygame.Surface(
            (SCREEN_WIDTH_DEFAULT, SCREEN_HEIGHT_DEFAULT)
        )
        self.day_night_surface.set_alpha(0)
        self.day_length = DAY_TIME
        self.night_length = NIGHT_TIME
        self.intersection_length = INTERSECTION_LENGTH
        self.time_elapsed = 0

        self.font_text_title = pygame.font.Font(
            (ASSET_PATH_FONT + FONT_TEXT + ".ttf"), 36
        )
        self.font_text_content = pygame.font.Font(
            (ASSET_PATH_FONT + FONT_TEXT + ".ttf"), 18
        )

        self.day_music = [f"{ASSET_MUSIC_DAY}{i}.mp3" for i in range(1, 163)]
        self.night_music = [f"{ASSET_MUSIC_NIGHT}{i}.mp3" for i in range(1, 58)]

        self.current_music = None
        self.is_day = True

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.default_volume)

        self.play_random_music(self.is_day)

    def update_volume(self, volume):
        self.current_volume = volume
        pygame.mixer.music.set_volume(self.current_volume)

    def play_random_music(self, is_day):
        if is_day:
            new_music = random.choice(self.day_music)
        else:
            new_music = random.choice(self.night_music)

        if new_music != self.current_music:
            self.update_volume(self.default_volume)
            pygame.mixer.music.load(new_music)
            pygame.mixer.music.play(loops=-1)
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
                self.update_volume(self.default_volume - self.default_volume * progress)
                self.day_night_surface.set_alpha(alpha)

                text = self.font_text_title.render(
                    "Night is coming", True, (255, 255, 255)
                )
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
                # Upgrade wave
                self.level.request_upgrade_wave()

            if current_time >= cycle_length - self.intersection_length:
                progress = (
                    current_time - (cycle_length - self.intersection_length)
                ) / self.intersection_length
                alpha = int(150 * (1 - progress))
                self.update_volume(self.default_volume - self.default_volume * progress)
                self.day_night_surface.set_alpha(alpha)
            else:
                self.day_night_surface.set_alpha(150)

        # Apply the day/night surface to the screen
        self.screen.blit(self.day_night_surface, (0, 0))

    def draw_day_night_bar(self):
        cycle_length = self.day_length + self.night_length
        current_time = self.time_elapsed % cycle_length

        if current_time < self.day_length:
            progress = current_time / self.day_length
            label = "Day"
        else:
            progress = (current_time - self.day_length) / self.night_length
            label = f"Night {self.night_count}"

        bar_width = 200
        bar_height = 20
        filled_width = int(bar_width * progress)

        if self.is_day:
            pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, bar_width, bar_height))
            pygame.draw.rect(
                self.screen, (255, 255, 255), (10, 10, filled_width, bar_height)
            )
        elif self.is_day == False:
            pygame.draw.rect(
                self.screen, (255, 255, 255), (10, 10, bar_width, bar_height)
            )
            pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, filled_width, bar_height))

        text_white = self.font_text_content.render(label, True, (255, 255, 255))
        text_black = self.font_text_content.render(label, True, (0, 0, 0))

        text_rect = text_white.get_rect(
            center=(10 + bar_width // 2, 10 + bar_height // 2)
        )

        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            self.screen.blit(text_black, text_rect.move(offset))

        self.screen.blit(text_white, text_rect)
        if current_time >= self.day_length and self.is_day:
            self.night_count += 1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            dt = self.clock.tick() / 1000

            self.level.run(dt)

            if self.level.game_started and self.level.game_over == False:
                self.update_day_night_cycle(dt)
                self.draw_day_night_bar()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
