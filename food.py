import variables as v
import random
import pygame
import food_behavior as fb
from pygame.math import Vector2
from rect_functions import *

class Food:
    def __init__(self):
        '''инициализация еды'''
        self.rectangle = pygame.Rect([0, 0, v.block_size, v.block_size])
        self.color = v.food_colors

    def randomize_food(self):
        '''создание рандомной еды с рандомным расположением прямоугольника и с рандомным выбором цвета'''
        self.rectangle = pygame.Rect([random.randint(v.border_width, v.width_of_screen - v.border_width), random.randint(v.border_width, v.width_of_screen - v.border_width), v.block_size, v.block_size])
        self.color = random.choice(v.food_colors)
        return self

    def draw_food(self, display):
        '''отрисовка еды на display'''
        pygame.draw.rect(display, self.color, self.rectangle)
    
    def clear_food(self, display):
        '''очистка display от еды'''
        pygame.draw.rect(display, v.background_color, self.rectangle)

    def intersect_level(self, level):
        '''проверка на пересечение еды с другими объектами из уровня level'''
        for i in level.level_borders:
            if self.rectangle.colliderect(i):
                return True
        for i in level.level_walls:
            if self.rectangle.colliderect(i.rectangle):
                return True
        for i in level.level_food:
            if self.rectangle.colliderect(i.rectangle):
                return True
        return False
    
    def intersect_snake(self, snake):
        '''проверка на пересечение еды со змейкой snake'''
        piece = pygame.Rect([snake.head.x, snake.head.y, v.block_size, v.block_size])
        if self.rectangle.colliderect(piece):
            return True
        current_piece_of_snake = snake.head + Vector2(v.block_size // 2, v.block_size // 2)
        for piece in range(len(snake.snake_body) - 1, -1, -1):
            current_piece_of_snake -= snake.snake_body[piece]
            if intersect_rect_with_rect_around_vector(self.rectangle, v.block_size // 2, current_piece_of_snake, snake.snake_body[piece]):
                return True
        return False


    def spawn_food_well_in_game(self, level, snake):
        '''создание еды на уровне level, где находится змейка snake таким образом, чтобы еда не пересесекалась ни с одним объектом из level, ни со змейкой,
        при неудачном количестве попыток генерации, не превышающем v.max_unsuccessful_attemts_for_food_spawn, возвращает сгенерированную еду, иначе None
        используется во время активного игрового процесса'''
        new_food = Food().randomize_food()
        count = 0
        while ((new_food.intersect_level(level) or new_food.intersect_snake(snake)) and count < v.max_unsuccessful_attemts_for_food_spawn):
            new_food = Food().randomize_food()
            count += 1
        if count < v.max_unsuccessful_attemts_for_food_spawn:
            level.level_food.append(new_food)
            return new_food
        return None

    def spawn_food_well(self, level):
        '''создание еды на уровне level до начала игры, то есть на этапе генерации уровня
        создание еды на уровне level таким образом, чтобы еда не пересесекалась ни с одним объектом из level, ни со змейкой,
        при неудачном количестве попыток генерации, не превышающем v.max_unsuccessful_attemts_for_food_spawn, возвращает сгенерированную еду, иначе None'''
        new_food = Food().randomize_food()
        count = 0
        while (new_food.intersect_level(level) and count < v.max_unsuccessful_attemts_for_food_spawn):
            new_food = Food().randomize_food()
            count += 1
        if count < v.max_unsuccessful_attemts_for_food_spawn:
            level.level_food.append(new_food)
            return new_food
        return None
    
    
    def food_behavior(self, snake, change_vector):
        '''запуск результата взаимодействия еды и змейки при взаимодействии со змейкой snake, которая будет сдвинута на вектор change_vector
        выбирается рандомный класс поведения из списка food_behavior'''
        food_behavior = [fb.PlusLengthToSnake(), fb.PlusLengthToSnake(), fb.PlusLengthToSnake(), fb.MinusLengthToSnake(), fb.SpeedBoost(), fb.SlowDown(), fb.BeautifulSnake(), fb.RainbowSnake()]
        behavior = random.choice(food_behavior)
        behavior.behave(snake, change_vector)