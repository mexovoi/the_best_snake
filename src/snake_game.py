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

        self.dis = pygame.display.set_mode((v.WIDTH_OF_SCREEN, v.HIGHT_OF_SCREEN))
        self.back_buffer = pygame.Surface((v.WIDTH_OF_SCREEN, v.HIGHT_OF_SCREEN))
        self.snake_buffer = pygame.Surface((v.WIDTH_OF_SCREEN, v.HIGHT_OF_SCREEN))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", v.SIZE_OF_FONT_FOR_SCORE)
        self.score_rect = self.back_buffer.get_rect(topleft=(0, 0))
        self.prev_score = 0

        self.game_over = False

        self.snake = Snake()

        self.change_vector = Vector2(0, 0)
        self.copy_rainbow_snake = v.RAINBOW_SNAKE
        self.copy_beautiful_snake = v.BEAUTIFUL_SNAKE
        return self.game_process()
        
        
    def score(self, score_number, level):
        '''обновление счетчика score'''
        pygame.draw.rect(self.back_buffer, v.BORDER_COLOR, level.level_borders[0])
        score_on_disp = self.font.render(f"Score: {score_number}", True, v.SCORE_IN_GAME_COLOR)
        self.back_buffer.blit(score_on_disp, self.score_rect)
        self.prev_score = score_number

    def game_process(self):
        '''запуск игрового процесса и сам игровой процесс до момента окончания игры'''
        level = LevelGenerator(v.WIDTH_OF_SCREEN // v.BLOCK_SIZE, v.HIGHT_OF_SCREEN // v.BLOCK_SIZE, v.BLOCK_SIZE, v.BORDER_WIDTH)
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
            if time_after_previous_spawn_food_moment == v.FRAMES_BETWEEN_FOOD_SPAWNS:
                time_after_previous_spawn_food_moment = 0
                new_food = Food().spawn_food_well_in_game(level, self.snake)
                if new_food != None:
                    new_food.draw_food(self.back_buffer)
            time_after_previous_spawn_food_moment += 1
            if (time_after_previous_speed_boost >= v.FRAMES_BETWEEN_SPEED_BOOSTS + (self.snake.snake_speed - v.SNAKE_START_SPEED) * v.INCREASE_FRAMES_BETWEEN_SPEED_BOOSTS):
                if self.snake.snake_speed < v.MAX_SNAKE_SPEED:
                    self.snake.snake_speed += 1
                time_after_previous_speed_boost = 0
            time_after_previous_speed_boost += 1
            self.score(self.snake.length_of_snake, level)
            self.dis.blit(self.back_buffer, (0, 0))
            pygame.display.flip()
            self.clock.tick(v.FPS)
        
        self.prev_score = self.snake.length_of_snake
        v.RAINBOW_SNAKE = self.copy_rainbow_snake
        v.BEAUTIFUL_SNAKE = self.copy_beautiful_snake
        pygame.quit()