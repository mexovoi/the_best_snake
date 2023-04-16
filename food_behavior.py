import abc
import variables as v
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
            snake.snake_body.appendleft(Vector2(v.block_size * signum(snake.snake_body[0].x), v.block_size * signum(snake.snake_body[0].y)))
            snake.length_of_snake += 1
        else:
            snake.snake_body.appendleft(Vector2(v.block_size * signum(change_vector.x), v.block_size * signum(change_vector.y)))
            snake.length_of_snake += 1
        pass

class MinusLengthToSnake(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''уменьшает длину змейки на v.block_size, в случае, если змейка длины 0, не делает ничего'''
        len_change_vector = v.block_size
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
        if (snake.snake_speed < v.max_snake_speed):
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
        v.beautiful_snake = not v.beautiful_snake
        pass
    
class RainbowSnake(BehaviorOfFood):
    def behave(self, snake, change_vector: Vector2):
        '''активирует радужный режим змейки, теперь при ее отрисовке все ее тело будет краситься в рандомные цвета радуги'''
        v.rainbow_snake = not v.rainbow_snake
        pass