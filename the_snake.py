from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
LINE_SIZE = 1
START = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Класс GameObject родительский класс игровых объектов"""

    def __init__(self, body_color=SNAKE_COLOR, position=START):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Абстрактный метод для переназначения в дочерних классах"""
        pass


class Apple(GameObject):
    """Класс Apple описывает экземпляры еды для змейки"""

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Задает случайное место появления еды"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка экземпляров еды"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake описывает экземпляр змеи, её отрибутов и методов"""

    def __init__(self, position=START):
        super().__init__(position)
        self.body_color = SNAKE_COLOR
        self.positions = [position, ]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = self.positions[-1]

    def draw(self):
        """Отрисовка экземпляра змеи"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Метод экземпляра для выпонления движения"""
        head_x, head_y = self.get_head_position()
        for move in (RIGHT, LEFT, UP, DOWN):
            if move == self.direction:
                m_x, m_y = move
                head_x += m_x * GRID_SIZE
                head_y += m_y * GRID_SIZE
                if head_x < 0:
                    head_x = SCREEN_WIDTH - GRID_SIZE
                elif head_x == SCREEN_WIDTH:
                    head_x = 0
                elif head_y < 0:
                    head_y = SCREEN_HEIGHT - GRID_SIZE
                elif head_y == SCREEN_HEIGHT:
                    head_y = 0
        self.positions.insert(0, (head_x, head_y))
        if len(self.positions) > self.length:
            self.positions.pop(-1)

    def get_head_position(self):
        """Метод возвращает положения головы"""
        return self.positions[0]

    def update_direction(self):
        """Метод изменения направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод для возвращения аттрибутов экземпляра"""
        self.positions = [self.position, ]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        self.length = 1


def handle_keys(game_object):
    """Функция выполнения действий при нажатии"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Игровой процесс"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(10)

    # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        # Змейка съела яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            check_position = True
            while check_position:
                if apple.position not in snake.positions:
                    check_position = False
                else:
                    apple.position = apple.randomize_position()
                    continue
        # Змейка съела саму себя
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
