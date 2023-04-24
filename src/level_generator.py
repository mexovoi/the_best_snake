import pygame
import src.variables as v
from src.food import Food
from src.walls import Walls

class LevelGenerator:
    def __init__(self, width, height, block_size, border_size):
        '''инициализация пустого уровня'''
        self.width = width
        self.height = height
        self.block_size = block_size
        self.border_size = border_size
        self.level_borders = []
        self.level_walls = []
        self.level_food = []

    def generate_borders(self):
        '''создание списка границ уровня'''
        top_rect = pygame.Rect(0, 0, v.width_of_screen, v.border_width)
        bottom_rect = pygame.Rect(0, v.hight_of_screen - v.border_width, v.width_of_screen, v.border_width)
        left_rect = pygame.Rect(0, v.border_width, v.border_width, v.hight_of_screen - v.border_width * 2)
        right_rect = pygame.Rect(v.width_of_screen - v.border_width, v.border_width, v.border_width, v.hight_of_screen - v.border_width * 2)
        self.level_borders = [top_rect, bottom_rect, left_rect, right_rect]

    def generate_food(self):
        '''генерация не более чем v.max_start_amount_of_food еды на уровне без пересечения с другими элементами уровня и запись в список еды уровня'''
        for i in range(v.max_start_amount_of_food):
            Food().spawn_food_well(self)
    
    def generate_walls(self):
        '''генерация не более чем v.max_start_amount_of_walls стенок на уровне без пересечения с другими элементами уровня и начальным положением змейки и запись в список стенок уровня'''
        for i in range(v.max_start_amount_of_walls):
            wall = Walls().spawn_wall_well()
            if wall != None:
                self.level_walls.append(wall)
    
    def generate_level(self):
        '''генерация уровня'''
        self.generate_borders()
        self.generate_walls()
        self.generate_food()

    def draw_level(self, screen):
        '''отрисовка на screen объектов уровня'''
        screen.fill(v.background_color)
        for obj in self.level_borders:
            pygame.draw.rect(screen, v.border_color, obj)
        for obj in self.level_food:
            obj.draw_food(screen)
        for obj in self.level_walls:
            obj.draw_wall(screen)
        pygame.display.flip()