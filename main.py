import sys
import random

import pygame

from utils import display_text
from player import Player
from obstacle import Obstacle

class Game:
    def __init__(self):
        # setup pygame
        pygame.init()
        pygame.display.set_caption('Title')
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.is_fullscreen = False
        self.screen_size = (1280, 720)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.screen_bg_color = (255, 255 ,255)
        self.is_game_played = False
        self.is_game_active = False

    def game_setup(self):
        # setup player
        self.player = Player(
                position = pygame.math.Vector2(self.screen.get_width() * 0.3, self.screen.get_height() * 0.5),
                velocity = pygame.math.Vector2(0, 0),
                acceleration = pygame.math.Vector2(0, 0.55),
                size = (50, 50),
                color = (0, 0, 0)
            )

        # setup obstacles
        self.top_obstacles = []
        self.bottom_obstacles = []

        # setup timer
        self.spawn_obstacle = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_obstacle, 2000)
        
        # reset game state
        self.is_game_active = True
        self.is_game_played = True

        # reset score
        self.score = 0

    def create_obstacle(self, position_y):
        return Obstacle(
                position = pygame.math.Vector2(self.screen.get_width(), position_y),
                velocity = pygame.math.Vector2(-3, 0),
                size = (80, 1000),
                color = (0, 0, 0)
            )

    def remove_obstacles(self):
        self.top_obstacles = [top_obstacle for top_obstacle in self.top_obstacles if top_obstacle.rect.right > 0]
        self.bottom_obstacles = [bottom_obstacle for bottom_obstacle in self.bottom_obstacles if bottom_obstacle.rect.right > 0]

    def is_player_colliding(self):
        is_out_of_bounds = self.player.rect.top < 0 or self.player.rect.bottom > self.screen.get_height()
        is_colliding_with_obstacle = self.player.rect.collidelist(self.top_obstacles) > -1 or self.player.rect.collidelist(self.bottom_obstacles) > -1
        return is_out_of_bounds or is_colliding_with_obstacle

    def update_score(self):
        for obstacle in self.top_obstacles:
            if self.player.rect.centerx == obstacle.rect.centerx:
                self.score += 1

    def display_score(self):
        display_text(
            surf = self.screen,
            text = f'{self.score}',
            size = 600,
            position = (self.screen.get_width() / 2, self.screen.get_height() / 2),
            color = (230, 230, 230)
        )

    def display_title_text(self):
        display_text(
            surf = self.screen,
            text = 'FLAPPY BIRD',
            size = 250,
            position = (self.screen.get_width() / 2, self.screen.get_height() / 2),
            color = (0, 0, 0),
        )

    def display_play_game_text(self):
        display_text(
            surf = self.screen,
            text = 'Click or press space to play',
            size = 40,
            position = (self.screen.get_width() / 2, self.screen.get_height() / 2 + 200), 
            color = (200, 200, 200),
            )

    def display_game_over_text(self):
        display_text(
            surf = self.screen,
            text = 'GAME OVER',
            size = 200,
            position = (self.screen.get_width() / 2, self.screen.get_height() / 2),
            color = (0, 0, 0)
        )

    def display_game_over_score_text(self):
        display_text(
            surf = self.screen,
            text = f'Score: {self.score}',
            size = 60,
            position = (self.screen.get_width() / 2, self.screen.get_height() / 2 + 110),
            color = (0, 0, 0)
        )

    def display_play_again_text(self):
        display_text(
            surf = self.screen,
            text = 'Click or press space to play again',
            size = 40,
            position = (self.screen.get_width() / 2, self.screen.get_height() / 2 + 200),
            color = (200, 200, 200)
        )

    def run(self):
        # game loop
        while True:
            # event loop
            for event in pygame.event.get():
                # handle closing window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # handle resizing
                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
                # toggle fullscreen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.is_fullscreen = not self.is_fullscreen
                    if self.is_fullscreen:
                        self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
                
                if self.is_game_active:
                    # handle obstacle spawning
                    if event.type == self.spawn_obstacle:
                        gap = 160
                        center_y = random.uniform(self.screen.get_height() / 2 - 250, self.screen.get_height() / 2 + 250)
                        top_obstacle = self.create_obstacle(center_y - gap / 2 - 1000)
                        bottom_obstacle = self.create_obstacle(center_y + gap / 2)

                        self.top_obstacles.append(top_obstacle)
                        self.bottom_obstacles.append(bottom_obstacle)
                else:
                    # handle starting game
                    is_space_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    is_mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN
                    if  is_space_pressed or is_mouse_clicked:
                        self.game_setup()

            # clear screen
            self.screen.fill(self.screen_bg_color)

            if self.is_game_active:
                # update and display score
                self.update_score()
                self.display_score()

                # update player
                self.player.update(self.screen)

                # update obstacles
                for top_obstacle, bottom_obstacle in zip(self.top_obstacles, self.bottom_obstacles):
                    top_obstacle.update(self.screen)
                    bottom_obstacle.update(self.screen)
                self.remove_obstacles()
                
                # check if player is colliding
                self.is_game_active = not self.is_player_colliding()
            else:
                if not self.is_game_played:
                    self.display_title_text()
                    self.display_play_game_text()
                else:
                    self.screen.fill(self.screen_bg_color)

                    self.display_game_over_text()
                    self.display_game_over_score_text()
                    self.display_play_again_text()
                    

            pygame.display.update()
            self.clock.tick(self.max_fps)

if __name__ == '__main__':
    game = Game()
    game.run()