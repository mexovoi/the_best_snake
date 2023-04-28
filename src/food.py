import src.variables as v
import random
import pygame
import src.food_behavior as fb
from pygame.math import Vector2
from src.rect_functions import *

class Food:
    def __init__(self):
        '''инициализация еды'''
        self.rectangle = pygame.Rect([0, 0, v.BLOCK_SIZE, v.BLOCK_SIZE])
        self.color = v.FOOD_COLORS

    def randomize_food(self):
        '''создание рандомной еды с рандомным расположением прямоугольника и с рандомным выбором цвета'''
        self.rectangle = pygame.Rect([random.randint(v.BORDER_WIDTH, v.WIDTH_OF_SCREEN - v.BORDER_WIDTH), random.randint(v.BORDER_WIDTH, v.WIDTH_OF_SCREEN - v.BORDER_WIDTH), v.BLOCK_SIZE, v.BLOCK_SIZE])
        self.color = random.choice(v.FOOD_COLORS)
        return self

    def draw_food(self, display):
        '''отрисовка еды на display'''
        pygame.draw.rect(display, self.color, self.rectangle)
    
    def clear_food(self, display):
        '''очистка display от еды'''
        pygame.draw.rect(display, v.BACKGROUND_COLOR, self.rectangle)

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
        piece = pygame.Rect([snake.head.x, snake.head.y, v.BLOCK_SIZE, v.BLOCK_SIZE])
        if self.rectangle.colliderect(piece):
            return True
        current_piece_of_snake = snake.head + Vector2(v.BLOCK_SIZE // 2, v.BLOCK_SIZE // 2)
        for piece in range(len(snake.snake_body) - 1, -1, -1):
            current_piece_of_snake -= snake.snake_body[piece]
            if intersect_rect_with_rect_around_vector(self.rectangle, v.BLOCK_SIZE // 2, current_piece_of_snake, snake.snake_body[piece]):
                return True
        return False


    def spawn_food_well_in_game(self, level, snake):
        '''создание еды на уровне level, где находится змейка snake таким образом, чтобы еда не пересесекалась ни с одним объектом из level, ни со змейкой,
        при неудачном количестве попыток генерации, не превышающем v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_FOOD_SPAWN, возвращает сгенерированную еду, иначе None
        используется во время активного игрового процесса'''
        new_food = Food().randomize_food()
        count = 0
        while ((new_food.intersect_level(level) or new_food.intersect_snake(snake)) and count < v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_FOOD_SPAWN):
            new_food = Food().randomize_food()
            count += 1
        if count < v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_FOOD_SPAWN:
            level.level_food.append(new_food)
            return new_food
        return None

    def spawn_food_well(self, level):
        '''создание еды на уровне level до начала игры, то есть на этапе генерации уровня
        создание еды на уровне level таким образом, чтобы еда не пересесекалась ни с одним объектом из level, ни со змейкой,
        при неудачном количестве попыток генерации, не превышающем v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_FOOD_SPAWN, возвращает сгенерированную еду, иначе None'''
        new_food = Food().randomize_food()
        count = 0
        while (new_food.intersect_level(level) and count < v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_FOOD_SPAWN):
            new_food = Food().randomize_food()
            count += 1
        if count < v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_FOOD_SPAWN:
            level.level_food.append(new_food)
            return new_food
        return None
    
    
    def food_behavior(self, snake, change_vector):
        '''запуск результата взаимодействия еды и змейки при взаимодействии со змейкой snake, которая будет сдвинута на вектор change_vector
        выбирается рандомный класс поведения из списка food_behavior'''
        food_behavior = [fb.PlusLengthToSnake(), fb.PlusLengthToSnake(), fb.PlusLengthToSnake(), fb.MinusLengthToSnake(), fb.SpeedBoost(), fb.SlowDown(), fb.BeautifulSnake(), fb.RainbowSnake()]
        behavior = random.choice(food_behavior)
        behavior.behave(snake, change_vector)