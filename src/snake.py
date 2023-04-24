import pygame
import src.variables as v
import random
from pygame.math import Vector2
from collections import deque
from src.level_generator import LevelGenerator
from src.rect_functions import *

def cross_product(a: Vector2, b: Vector2):
    '''возвращает длину векторного произведения двух векторов с учетом направления'''
    return a.x * b.y - a.y * b.x

def signum(a: int):
    '''возвращает знак числа, 1 если число положительное, -1 если отрицательное, 0 если число 0'''
    if a > 0:
        return 1
    if a < 0:
        return -1
    if a == 0:
        return 0

def color(color, is_random_color):
    '''если is_random_color True, то возвращает рандомый цвет из списка v.rainbow_colors, иначе возвращает переданный цвет color'''
    if is_random_color:
        return random.choice(v.rainbow_colors)
    else:
        return color

def draw_rect_around_point(display, color, width_of_zone, center: Vector2):
    '''отрисовка квадрата цвета color с с центром в center и длиной стороны width_of_zone * 2 на display'''
    pygame.draw.rect(display, color, make_rectangle(center.x, center.y, width_of_zone, width_of_zone))
    pygame.draw.rect(display, color, make_rectangle(center.x, center.y, -width_of_zone, width_of_zone))
    pygame.draw.rect(display, color, make_rectangle(center.x, center.y, width_of_zone, -width_of_zone))
    pygame.draw.rect(display, color, make_rectangle(center.x, center.y, -width_of_zone, -width_of_zone))

def draw_rect_around_vector(display, color,  width_of_zone, start_point: Vector2, skeleton_of_rect: Vector2):
    '''отрисовка прямоугольника цвета color на display являющегося результатом движения квадрата с центром в start_point с длиной стороны width_of_zone * 2 вдоль вектора skeleton_of_rect'''
    draw_rect_around_point(display, color, width_of_zone - v.snake_start_speed * v.beautiful_snake, start_point)
    draw_rect_around_point(display, color, width_of_zone - v.snake_start_speed * v.beautiful_snake, start_point + skeleton_of_rect)
    if skeleton_of_rect.x == 0:
        pygame.draw.rect(display, color, make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x + width_of_zone, skeleton_of_rect.y))
        pygame.draw.rect(display, color, make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x - width_of_zone, skeleton_of_rect.y))
    if skeleton_of_rect.y == 0:
        pygame.draw.rect(display, color, make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x, width_of_zone))
        pygame.draw.rect(display, color, make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x, -width_of_zone))

class Snake:
    def __init__(self):
        '''инициализация змейки с заданием ее начальной скорости v.start_snake_speed с толщиной тела змейик v.block_size,
        начальным положением верхнего левого угла головы в self.head и начальной длиной змейки 0'''
        self.snake_speed = v.snake_start_speed
        self.block_size = v.block_size
        self.head = Vector2(v.start_position_of_snake_x_coord, v.start_position_of_snake_y_coord)
        self.snake_body = deque()
        self.length_of_snake = 0
    
    def clear_display_from_snake(self, display):
        '''очищение display от тела змейки self'''
        pygame.draw.rect(display, v.background_color, [self.head.x, self.head.y, v.block_size, v.block_size])
        current_piece_of_snake = self.head + Vector2(v.block_size // 2, v.block_size // 2)
        for piece in range(len(self.snake_body) - 1, -1, -1):
            current_piece_of_snake -= self.snake_body[piece]
            draw_rect_around_vector(display, v.background_color, v.block_size // 2, current_piece_of_snake, self.snake_body[piece])

    def draw_snake(self, display):
        '''отрисовка тела змейки на display'''
        pygame.draw.rect(display, color(v.snake_color, v.rainbow_snake), [self.head.x, self.head.y, v.block_size, v.block_size])
        current_piece_of_snake = self.head + Vector2(v.block_size // 2, v.block_size // 2)
        for piece in range(len(self.snake_body) - 1, -1, -1):
            current_piece_of_snake -= self.snake_body[piece]
            draw_rect_around_vector(display, color(v.snake_color, v.rainbow_snake), v.block_size // 2, current_piece_of_snake, self.snake_body[piece])

    def move_snake(self, change_vector: Vector2):
        '''подвинуть змейку на вектор change_vector'''
        len_change_vector = abs(change_vector.x) + abs(change_vector.y)
        self.snake_body.append(change_vector.copy())
        self.head += change_vector
        while len_change_vector > 0:
            if abs(self.snake_body[0].x) + abs(self.snake_body[0].y) <= len_change_vector:
                len_change_vector -= (abs(self.snake_body[0].x) + abs(self.snake_body[0].y))
                self.snake_body.popleft()
            else:
                self.snake_body[0] -= Vector2(Vector2(signum(self.snake_body[0].x), signum(self.snake_body[0].y)) * len_change_vector)
                len_change_vector = 0

    def new_piece_of_snake(self, change_vector: Vector2):
        '''возвращает прямоугольник, который является новым куском змейки,
        которого не было раньше при сдвиге змейки на вектор change_vector,тело змейки еще не сдвинуто на вектор change_vector'''
        copy_change_vector = change_vector.copy()
        copy_head = self.head.copy()
        if change_vector.x < 0:
            copy_head.x += change_vector.x
            copy_change_vector.x *= -1
        if change_vector.y < 0:
            copy_head.y += change_vector.y
            copy_change_vector.y *= -1
        if change_vector.x == 0:
            copy_change_vector.x = v.block_size
            copy_change_vector.y = max(copy_change_vector.y, v.block_size)
        if change_vector.y == 0:
            copy_change_vector.y = v.block_size
            copy_change_vector.x = max(copy_change_vector.x, v.block_size)
        return pygame.Rect([copy_head.x, copy_head.y, copy_change_vector.x, copy_change_vector.y])

    def intersect_walls(self, walls, change_vector: Vector2):
        '''проверка пересечения змейки со стенками из списка стенок walls при сдвиге змейки на вектор change_vector, змейка считается еще не сдвинутой'''
        new_piece_of_snake = self.new_piece_of_snake(change_vector)
        for wall in walls:
            if new_piece_of_snake.colliderect(wall.rectangle):
                return True
        return False
    
    def intersect_border(self, borders, change_vector: Vector2):
        '''проверка пересечения змейки с границами уровня из списка borders при сдвиге змейки на вектор change_vector, змейка считается еще не сдвинутой'''
        new_piece_of_snake = self.new_piece_of_snake(change_vector)
        for border in borders:
            if new_piece_of_snake.colliderect(border):
                return True
        return False
    
    def intersect_food(self, food, change_vector: Vector2, display):
        '''проверка пересечения змейки с едой из списка food при сдвиге на вектор change_vector
        в случае пересечения змейки с едой запуск взаимодействия food_behavior и отображение результата на display'''
        new_piece_of_snake = self.new_piece_of_snake(change_vector)
        apple = 0
        while apple < len(food):
            if new_piece_of_snake.colliderect(food[apple].rectangle):
                food[apple].food_behavior(self, change_vector)
                food[apple].clear_food(display)
                del food[apple]
                apple -= 1
            apple += 1
    
    def go_back(self, change_vector: Vector2):
        '''проверка того, что змейка не идет назад'''
        if self.length_of_snake == 0 or len(self.snake_body) == 0:
            return False
        if cross_product(self.snake_body[-1], change_vector) == 0 and change_vector.dot(self.snake_body[-1]) < 0:
            return True
    
    def intersect_self(self, change_vector: Vector2):
        '''проверка змейки на самопересечение при сдвиге на change_vector, считается, что змейка уже была сдвинута'''
        if self.length_of_snake == 0 or len(self.snake_body) == 0 or abs(self.snake_body[-1].x) == v.block_size or abs(self.snake_body[-1].y) == v.block_size:
            return False
        if change_vector.x == 0 and change_vector.y > 0:
            new_piece_of_snake = make_rectangle(-v.block_size // 2, v.block_size // 2 - change_vector.y, v.block_size, change_vector.y)
        elif change_vector.x == 0 and change_vector.y < 0:
            new_piece_of_snake = make_rectangle(-v.block_size // 2, -v.block_size // 2, v.block_size, -change_vector.y)
        elif change_vector.x < 0 and change_vector.y == 0:
            new_piece_of_snake = make_rectangle(-v.block_size // 2, -v.block_size // 2, -change_vector.x, v.block_size)
        elif change_vector.x > 0 and change_vector.y == 0:
            new_piece_of_snake = make_rectangle(v.block_size // 2 - change_vector.x, -v.block_size // 2, change_vector.x, v.block_size)
        current_piece_of_snake = -self.snake_body[-1]
        for piece in range(len(self.snake_body) - 2, -1, -1):
            current_piece_of_snake -= self.snake_body[piece]
            if intersect_rect_with_rect_around_vector(new_piece_of_snake, v.block_size // 2, current_piece_of_snake, self.snake_body[piece]):
                return True
        return False