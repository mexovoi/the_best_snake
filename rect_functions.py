import pygame
from pygame.math import Vector2
import variables as v

def make_rectangle(left_top_corner_x, left_top_corner_y, size_x, size_y):
        '''создание прямоугольника с координатами левого верхнего угла с координатами left_top_corner_x по оси x и left_top_corner_y по оси y
        с длинами сторон size_x и size_y по осям x и y, при этом size_x и size_y могут быть отрицательными, результат будет соответствующим'''
        reference_point = Vector2(left_top_corner_x, left_top_corner_y)
        diag_vector = Vector2(size_x, size_y)
        if diag_vector.x < 0:
            reference_point.x += diag_vector.x
            diag_vector.x *= -1
        if diag_vector.y < 0:
            reference_point.y += diag_vector.y
            diag_vector.y *= -1
        return pygame.Rect([reference_point.x, reference_point.y, diag_vector.x, diag_vector.y])

def intersect_rect_with_rect_around_point(rect_one, width_of_zone, center: Vector2):
    '''проверка пересечения прямоугольника rect_one и квадрата с центром center и длиной стороны width_of_zone * 2'''
    answer = False
    answer = answer or rect_one.colliderect(make_rectangle(center.x, center.y, width_of_zone, width_of_zone))
    answer = answer or rect_one.colliderect(make_rectangle(center.x, center.y, -width_of_zone, width_of_zone))
    answer = answer or rect_one.colliderect(make_rectangle(center.x, center.y, width_of_zone, -width_of_zone))
    answer = answer or rect_one.colliderect(make_rectangle(center.x, center.y, -width_of_zone, -width_of_zone))
    return answer

def intersect_rect_with_rect_around_vector(rect_one, width_of_zone, start_point: Vector2, skeleton_of_rect: Vector2):
    '''проверка пересечения прямоугольника rect_one с прямогульником образованным движением квадрата с центром в start_point с длиной стороны width_of_zone * 2
    при его движении на вектор skelet_of_rect'''
    answer = False
    answer = answer or intersect_rect_with_rect_around_point(rect_one, width_of_zone - v.snake_start_speed * v.beautiful_snake, start_point)
    intersect_rect_with_rect_around_point(rect_one, width_of_zone - v.snake_start_speed * v.beautiful_snake, start_point + skeleton_of_rect)
    if skeleton_of_rect.x == 0:
        answer = answer or rect_one.colliderect(make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x + width_of_zone, skeleton_of_rect.y))
        answer = answer or rect_one.colliderect(make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x - width_of_zone, skeleton_of_rect.y))
    if skeleton_of_rect.y == 0:
        answer = answer or rect_one.colliderect(make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x, width_of_zone))
        answer = answer or rect_one.colliderect(make_rectangle(start_point.x, start_point.y, skeleton_of_rect.x, -width_of_zone))
    return answer