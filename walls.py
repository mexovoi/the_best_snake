import random
import pygame
import variables as v

class Walls:
    def __init__(self):
        '''инициализация стенки размера v.block_size с рандомным направлением'''
        self.rectangle = pygame.Rect([0, 0, v.block_size, v.block_size])
        self.color = "black"
        self.orientation_of_rect = random.choice(["vertical", "gorisontal"])

    def randomize_wall(self):
        '''создание произвольной стенки произвольной длины и с рандомным расположением с заданным на этапе инициализации направлением'''
        if self.orientation_of_rect == "vertical":
            self.rectangle = pygame.Rect([random.randint(v.border_width, v.width_of_screen - v.border_width - v.block_size),
                                          random.randint(v.border_width, v.width_of_screen - v.border_width - v.block_size),
                                          random.randint(v.block_size, v.max_wall_random_length), v.block_size])
        if self.orientation_of_rect == "gorisontal":
            self.rectangle = pygame.Rect([random.randint(v.border_width, v.width_of_screen - v.border_width - v.block_size),
                                          random.randint(v.border_width, v.width_of_screen - v.border_width - v.block_size),
                                          v.block_size, random.randint(v.block_size, v.max_wall_random_length)])
        return self

    def draw_wall(self, display):
        '''отрисовка стенки'''
        pygame.draw.rect(display, self.color, self.rectangle)

    def spawn_wall_well(self):
        '''создание стенки с учетом направления таким образом, чтобы стенка не пересекалась с уже созданными объектами на уровне и с начальным положением змейки
        если было сделано v.max_unsuccessful_attemts_for_wall_spawn неудачных попыток генерации стенки, возвращает None, иначе возвращает саму новую стенку'''
        new_wall = Walls().randomize_wall()
        attempts = 0
        while new_wall.rectangle.colliderect([v.start_position_of_snake_x_coord, v.start_position_of_snake_y_coord, v.block_size, v.block_size]) and attempts < v.max_unsuccessful_attemts_for_wall_spawn:
            new_wall = Walls().randomize_wall()
            attempts += 1
        if attempts == v.max_unsuccessful_attemts_for_wall_spawn:
            return None
        return new_wall