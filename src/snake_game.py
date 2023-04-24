import pygame
from pygame.math import Vector2
from src.snake import Snake
import src.variables as v
from src.food import Food
from src.level_generator import LevelGenerator

class SnakeGame:
    def __init__(self):
        '''создание игрового поля'''
        pygame.init()

        self.dis = pygame.display.set_mode((v.width_of_screen, v.hight_of_screen))
        self.back_buffer = pygame.Surface((v.width_of_screen, v.hight_of_screen))
        self.snake_buffer = pygame.Surface((v.width_of_screen, v.hight_of_screen))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", v.size_of_font_for_score)
        self.score_rect = self.back_buffer.get_rect(topleft=(0, 0))
        self.prev_score = 0

        self.game_over = False

        self.snake = Snake()

        self.change_vector = Vector2(0, 0)
        self.copy_rainbow_snake = v.rainbow_snake
        self.copy_beautiful_snake = v.beautiful_snake
        return self.game_process()
        
        
    def score(self, score_number, level):
        '''обновление счетчика score'''
        pygame.draw.rect(self.back_buffer, v.border_color, level.level_borders[0])
        score_on_disp = self.font.render(f"Score: {score_number}", True, v.score_in_game_color)
        self.back_buffer.blit(score_on_disp, self.score_rect)
        self.prev_score = score_number

    def game_process(self):
        '''запуск игрового процесса и сам игровой процесс до момента окончания игры'''
        level = LevelGenerator(v.width_of_screen // v.block_size, v.hight_of_screen // v.block_size, v.block_size, v.border_width)
        level.generate_level()
        level.draw_level(self.back_buffer)
        previous_event_key = None
        time_after_previous_spawn_food_moment = 0
        time_after_previous_speed_boost = 0
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = True
                        continue
                    elif event.key == pygame.K_LEFT and previous_event_key != pygame.K_RIGHT:
                        self.change_vector = Vector2(-self.snake.snake_speed, 0)
                        previous_event_key = event.key
                    elif event.key == pygame.K_RIGHT and previous_event_key != pygame.K_LEFT:
                        self.change_vector = Vector2(self.snake.snake_speed, 0)
                        previous_event_key = event.key
                    elif event.key == pygame.K_UP and previous_event_key != pygame.K_DOWN:
                        self.change_vector = Vector2(0, -self.snake.snake_speed)
                        previous_event_key = event.key
                    elif event.key == pygame.K_DOWN and previous_event_key != pygame.K_UP:
                        self.change_vector = Vector2(0, self.snake.snake_speed)
                        previous_event_key = event.key

            if self.snake.go_back(self.change_vector):
                self.change_vector *= -1
            if self.snake.intersect_walls(level.level_walls, self.change_vector):
                self.game_over = True
                continue
            if self.snake.intersect_border(level.level_borders, self.change_vector):
                self.game_over = True
                continue
            self.snake.clear_display_from_snake(self.back_buffer)
            self.snake.intersect_food(level.level_food, self.change_vector, self.back_buffer)
            self.snake.move_snake(self.change_vector)
            self.snake.draw_snake(self.back_buffer)
            if self.snake.intersect_self(self.change_vector):
                self.game_over = True
                continue
            if time_after_previous_spawn_food_moment == v.frames_between_food_spawns:
                time_after_previous_spawn_food_moment = 0
                new_food = Food().spawn_food_well_in_game(level, self.snake)
                if new_food != None:
                    new_food.draw_food(self.back_buffer)
            time_after_previous_spawn_food_moment += 1
            if (time_after_previous_speed_boost >= v.frames_between_speed_boosts + (self.snake.snake_speed - v.snake_start_speed) * v.increase_frames_between_speed_boosts):
                if self.snake.snake_speed < v.max_snake_speed:
                    self.snake.snake_speed += 1
                time_after_previous_speed_boost = 0
            time_after_previous_speed_boost += 1
            self.score(self.snake.length_of_snake, level)
            self.dis.blit(self.back_buffer, (0, 0))
            pygame.display.flip()
            self.clock.tick(v.fps)
        
        self.prev_score = self.snake.length_of_snake
        v.rainbow_snake = self.copy_rainbow_snake
        v.beautiful_snake = self.copy_beautiful_snake
        pygame.quit()