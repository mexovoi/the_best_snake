import random
import pygame
import src.variables as v

class Walls:
    def __init__(self):
        '''инициализация стенки размера v.BLOCK_SIZE с рандомным направлением'''
        self.rectangle = pygame.Rect([0, 0, v.BLOCK_SIZE, v.BLOCK_SIZE])
        self.color = "black"
        self.orientation_of_rect = random.choice(["vertical", "gorisontal"])

    def randomize_wall(self):
        '''создание произвольной стенки произвольной длины и с рандомным расположением с заданным на этапе инициализации направлением'''
        if self.orientation_of_rect == "vertical":
            self.rectangle = pygame.Rect([random.randint(v.BORDER_WIDTH, v.WIDTH_OF_SCREEN - v.BORDER_WIDTH - v.BLOCK_SIZE),
                                          random.randint(v.BORDER_WIDTH, v.WIDTH_OF_SCREEN - v.BORDER_WIDTH - v.BLOCK_SIZE),
                                          random.randint(v.BLOCK_SIZE, v.MAX_WALL_RANDOM_LENGTH), v.BLOCK_SIZE])
        if self.orientation_of_rect == "gorisontal":
            self.rectangle = pygame.Rect([random.randint(v.BORDER_WIDTH, v.WIDTH_OF_SCREEN - v.BORDER_WIDTH - v.BLOCK_SIZE),
                                          random.randint(v.BORDER_WIDTH, v.WIDTH_OF_SCREEN - v.BORDER_WIDTH - v.BLOCK_SIZE),
                                          v.BLOCK_SIZE, random.randint(v.BLOCK_SIZE, v.MAX_WALL_RANDOM_LENGTH)])
        return self

    def draw_wall(self, display):
        '''отрисовка стенки'''
        pygame.draw.rect(display, self.color, self.rectangle)

    def spawn_wall_well(self):
        '''создание стенки с учетом направления таким образом, чтобы стенка не пересекалась с уже созданными объектами на уровне и с начальным положением змейки
        если было сделано v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_WALL_SPAWN неудачных попыток генерации стенки, возвращает None, иначе возвращает саму новую стенку'''
        new_wall = Walls().randomize_wall()
        attempts = 0
        while new_wall.rectangle.colliderect([v.START_POSITION_OF_SNAKE_X_COORD, v.START_POSITION_OF_SNAKE_Y_COORD, v.BLOCK_SIZE, v.BLOCK_SIZE]) and attempts < v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_WALL_SPAWN:
            new_wall = Walls().randomize_wall()
            attempts += 1
        if attempts == v.MAX_UNSUCCESSFUL_ATTEMTS_FOR_WALL_SPAWN:
            return None
        return new_wall