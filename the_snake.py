from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

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
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс GameObject родительский класс игровых объектов"""

    def __init__(self, body_color=SNAKE_COLOR, position=START):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Абстрактный метод для переназначения в дочерних классах"""
        pass


class Apple(GameObject):
    """Класс Apple описывает экземпляры еды для змейки"""

    def __init__(self, body_color):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Задает случайное место появления еды"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка экземпляров еды"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake описывает экземпляр змеи, её отрибутов и методов"""

    def __init__(self, body_color, position=START):
        super().__init__(body_color, position)
        self.reset([RIGHT])
        self.last = self.positions[-1]

    def draw(self):
        """Отрисовка экземпляра змеи"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Метод экземпляра для выпонления движения"""
        head_x, head_y = self.get_head_position()
        for move in (RIGHT, LEFT, UP, DOWN):
            if move == self.direction:
                m_x, m_y = move
                head_x = (head_x + m_x * GRID_SIZE) % SCREEN_WIDTH
                head_y = (head_y + m_y * GRID_SIZE) % SCREEN_HEIGHT
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

    def reset(self, direction):
        """Метод для возвращения аттрибутов экземпляра"""
        self.positions = [self.position, ]
        self.direction = choice(direction)
        self.next_direction = None
        self.length = 1


def handle_keys(game_object):
    """Функция выполнения действий при нажатии"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Игровой процесс"""
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(10)

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
            snake.reset(DIRECTIONS)

        pg.display.update()


if __name__ == '__main__':
    main()
