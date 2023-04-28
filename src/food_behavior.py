import abc
import src.variables as v
from pygame.math import Vector2

def signum(a: int):
    if a > 0:
        return 1
    if a < 0:
        return -1
    if a == 0:
        return 0

class BehaviorOfFood(abc.ABC):
    '''абстрактный класс с методом behave, который запускает реакцию snake при съедании еды при сдвиге на вектор change_vector(сдвига еще не было)'''
    @abc.abstractmethod
    def behave(self, snake, change_vector: Vector2):
        pass

class PlusLengthToSnake(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''увеличивает длину змейки snake на v.bloc_size'''
        if len(snake.snake_body) > 0:
            snake.snake_body.appendleft(Vector2(v.BLOCK_SIZE * signum(snake.snake_body[0].x), v.BLOCK_SIZE * signum(snake.snake_body[0].y)))
            snake.length_of_snake += 1
        else:
            snake.snake_body.appendleft(Vector2(v.BLOCK_SIZE * signum(change_vector.x), v.BLOCK_SIZE * signum(change_vector.y)))
            snake.length_of_snake += 1
        pass

class MinusLengthToSnake(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''уменьшает длину змейки на v.BLOCK_SIZE, в случае, если змейка длины 0, не делает ничего'''
        len_change_vector = v.BLOCK_SIZE
        if snake.length_of_snake > 0:
            snake.length_of_snake -= 1
        while len_change_vector > 0 and len(snake.snake_body) > 0:
            if abs(snake.snake_body[0].x) + abs(snake.snake_body[0].y) <= len_change_vector:
                len_change_vector -= (abs(snake.snake_body[0].x) + abs(snake.snake_body[0].y))
                snake.snake_body.popleft()
            else:
                snake.snake_body[0] -= Vector2(Vector2(signum(snake.snake_body[0].x), signum(snake.snake_body[0].y)) * len_change_vector)
                len_change_vector = 0
        pass

class SpeedBoost(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''увеличивает скорость змейки на 1 пиксель в кадр'''
        if (snake.snake_speed < v.MAX_SNAKE_SPEED):
            snake.snake_speed += 1
        pass
    
class SlowDown(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''замедляет змейку на 1 пиксель в кадр'''
        if (snake.snake_speed > 1):
            snake.snake_speed -= 1
        pass
    
class BeautifulSnake(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''переключает режим отрисовка змейки на красивый, у змейки будет хвост и при поворотах будут некоторые шершавости'''
        v.BEAUTIFUL_SNAKE = not v.BEAUTIFUL_SNAKE
        pass
    
class RainbowSnake(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''активирует радужный режим змейки, теперь при ее отрисовке все ее тело будет краситься в рандомные цвета радуги'''
        v.RAINBOW_SNAKE = not v.RAINBOW_SNAKE
        pass