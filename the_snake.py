from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
Color = tuple[int, int, int]
Pointer = tuple[int, int]
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_OF_WIDTH = SCREEN_WIDTH // 2 - GRID_SIZE
CENTER_OF_HEIGHT = SCREEN_HEIGHT // 2 - GRID_SIZE

# Направления движения:
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 20

# Цвет объекта по умолчанию
DEFAULT_COLOR: Color = (0, 0, 0)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color: Color = DEFAULT_COLOR):
        self.position = CENTER_OF_WIDTH, CENTER_OF_HEIGHT
        self.body_color = body_color

    def draw(self):
        """Рисование объекта"""
        raise NotImplementedError('Создай метод для отрисовки объекта!')


class Apple(GameObject):
    """Класс управляет появлением яблока на поле."""

    def __init__(self, body_color: Color = APPLE_COLOR):
        super().__init__(body_color=body_color)

    def randomize_position(self, positions_snake):
        """Задаёт координаты яблока случайным образом."""
        while True:
            x = (
                randint(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE)
                // GRID_SIZE
            ) * GRID_SIZE
            y = (
                randint(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE)
                // GRID_SIZE
            ) * GRID_SIZE
            # Проверка попало ли яблоко на змейку
            if (x, y) not in positions_snake:
                break
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс управляет движением, ростом, столкновениями змейки."""

    def __init__(self, body_color: Color = SNAKE_COLOR):
        super().__init__(body_color=body_color)
        x = (
            randint(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        y = (
            randint(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        self.length = 1
        self.positions = []
        self.positions.append((x, y))
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Перезапуск игры при столкновении змейки с собой."""
        x = (
            randint(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        y = (
            randint(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        self.length = 1
        self.positions = []
        self.positions.append((x, y))
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self):
        """Обновляет координаты сегментов змейки."""
        x, y = self.get_head_position()
        x = (x + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        y = (y + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        self.positions.insert(0, (x, y))

    def update_direction(self):
        """Обновляет направление движение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake, apple):
    """Обрабатывает ввод с клавиатуры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if (
                event.key == pg.K_UP
                and snake.direction != DOWN
            ):
                snake.next_direction = UP
            elif (
                event.key == pg.K_DOWN
                and snake.direction != UP
            ):
                snake.next_direction = DOWN
            elif (
                event.key == pg.K_LEFT
                and snake.direction != RIGHT
            ):
                snake.next_direction = LEFT
            elif (
                event.key == pg.K_RIGHT
                and snake.direction != LEFT
            ):
                snake.next_direction = RIGHT
            snake.update_direction()
            snake.move()
            check_move(snake, apple)


def check_move(snake, apple):
    """Проверка условий движения."""
    # Проверка на столкновение змейки с яблоком.
    if snake.get_head_position() == apple.position:
        apple.randomize_position(snake.positions)
    else:
        snake.last = snake.positions.pop()
    # Проверка на столкновение змейки с собой.
    if snake.get_head_position() in snake.positions[1:]:
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.reset()
        apple.draw()
    # Отрисовка нового яблока, если старое съедено
    if len(snake.positions) > snake.length:
        apple.draw()
        snake.length += 1
    # Отрисовка змейки
    snake.draw()
    pg.display.update()


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pg.init()
    # Создание экземпляров классов
    apple = Apple()
    snake = Snake()
    apple.draw()
    snake.draw()
    pg.display.update()
    while True:
        # Задание скорости игры
        clock.tick(SPEED)
        # Управление змейкой
        handle_keys(snake, apple)


if __name__ == '__main__':
    main()
