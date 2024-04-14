from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
HEIGHT_INFO = 30
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

# Цвета еды и препятствий:
APPLE_COLOR = (255, 0, 0)
MUSHROOM_COLOR = (0, 0, 255)
STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет текста
TEXT_COLOR = (255, 255, 255)
INFO_COLOR = (198, 195, 181)

# Скорость движения змейки и условия повышения скорости:
START_SPEED = 10
LEVEL_UP = 70

# Настройка игрового окна:
screen = pg.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT + HEIGHT_INFO), 0, 32)
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

    def draw_cell(self, rect):
        """Метод отрисовки игровых объектов"""
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс Apple описывает экземпляры дополнительных объектов для змейки"""

    def __init__(self, body_color=BORDER_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Задает случайное место появления еды"""
        position_not_free = True
        while position_not_free:
            pos_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            pos_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if screen.get_at((pos_x, pos_y)) == BOARD_BACKGROUND_COLOR:
                position_not_free = False
        return (pos_x, pos_y)

    def draw(self):
        """Отрисовка экземпляров еды"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        self.draw_cell(rect)

    def reset(*args):
        """Метод для новых позиций еды и препятствий"""
        for object in args:
            object.position = object.randomize_position()


class Snake(GameObject):
    """Класс Snake описывает экземпляр змеи, её отрибутов и методов"""

    def __init__(self, body_color=SNAKE_COLOR, position=START):
        super().__init__(body_color, position)
        self.reset([RIGHT])
        self.last = self.positions[-1]

    def draw(self):
        """Отрисовка экземпляра змеи"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            self.draw_cell(rect)

    def move(self):
        """Метод экземпляра описания движения змейки"""
        head_x, head_y = self.get_head_position()
        m_x, m_y = self.direction
        head_x = (head_x + m_x * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + m_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (head_x, head_y))
        if len(self.positions) > self.length:
            self.positions.pop()

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
        self.speed = START_SPEED


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


def game_result(point, speed):
    """Функция изменения счета игры"""
    coefficient = 1 + (speed - 10)
    return point * coefficient


def game_over(snake, all_object, score):
    """Функция по описанию конца игры и запись результата"""
    file = open('game_result.txt', 'a')
    file.write(f'Счет: {score}, Скорость: {snake.speed}\n')
    file.close
    snake.reset(DIRECTIONS)
    for object in all_object:
        object.reset()
    return 0


def draw_text(score, speed):
    """Вывод счета на экран"""
    pg.draw.line(screen, INFO_COLOR, (0, 495), (640, 495), 30)
    pg.font.init()
    f1 = pg.font.Font(None, 35)
    text1 = f1.render(
        f'Счет:{str(score)} Скорость: {str(speed)}', 1, TEXT_COLOR)
    screen.blit(text1, (20, 485))


def main():
    """Игровой процесс"""
    score = 0
    apple = Apple(APPLE_COLOR)
    mushroom = Apple(MUSHROOM_COLOR)
    stone = Apple(STONE_COLOR)
    snake = Snake(SNAKE_COLOR)
    all_object = (apple, mushroom, stone)
    while True:
        clock.tick(snake.speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        draw_text(score, snake.speed)
        for object in all_object:
            object.draw()
        # Змейка съела яблоко, увеличение скорости после 70 яблок.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            if snake.length % LEVEL_UP == 0:
                snake.speed += 1
            score += game_result(10, snake.speed)
        elif snake.get_head_position() == mushroom.position:
            snake.length -= 1
            if snake.length == 0:
                game_over(snake, all_object, score)
                continue
            snake.positions.pop()
            mushroom.position = mushroom.randomize_position()
            score += game_result(-10, snake.speed)
        elif snake.get_head_position() == stone.position:
            score = game_over(snake, all_object, score)
        # Змейка съела саму себя
        elif snake.get_head_position() in snake.positions[1:]:
            score = game_over(snake, all_object, score)
        pg.display.update()


if __name__ == '__main__':
    main()
