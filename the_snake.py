from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_OF_WIDTH = SCREEN_WIDTH // 2 - GRID_SIZE
CENTER_OF_HEIGHT = SCREEN_HEIGHT // 2 - GRID_SIZE

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

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        self.position = CENTER_OF_WIDTH, CENTER_OF_HEIGHT
        self.body_color = (0, 0, 0)

    def draw(self):
        """Рисование объекта"""
        pass


class Apple(GameObject):
    """Класс управляет появлением яблока на поле."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Задаёт координаты яблока случайным образом."""
        x = (
            randint(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        y = (
            randint(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        self.position = (x, y)
        return x, y

    def draw(self):
        """Отрисовывает яблоко на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс управляет движением, ростом, столкновениями змейки."""

    def __init__(self, apple='apple'):
        super().__init__()
        x = (
            randint(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        y = (
            randint(GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE)
            // GRID_SIZE
        ) * GRID_SIZE
        self.apple = apple
        self.length = 1
        self.positions = []
        self.positions.append((x, y))
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = self.positions[-1]

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
        self.body_color = SNAKE_COLOR
        self.last = self.positions[-1]
        self.apple.draw()

    def move(self):
        """Обновляет координаты сегментов змейки."""
        x, y = self.get_head_position()
        dx = x + GRID_SIZE * self.direction[0]
        dy = y + GRID_SIZE * self.direction[1]
        if dx < 0:
            dx = SCREEN_WIDTH - GRID_SIZE
        elif dx % SCREEN_WIDTH == 0:
            dx = 0
        elif dy < 0:
            dy = SCREEN_HEIGHT - GRID_SIZE
        elif dy % SCREEN_HEIGHT == 0:
            dy = 0
        self.positions.insert(0, (dx, dy))
        # Проверка на столкновение змейки с яблоком.
        if self.positions[0] == self.apple.position:
            self.apple.randomize_position()
        else:
            self.last = self.positions.pop()
        # Проверка на столкновение змейки с собой.
        for position in self.positions[1:]:
            if position == self.positions[0]:
                screen.fill(BOARD_BACKGROUND_COLOR)
                self.reset()

    def update_direction(self):
        """Обновляет направление движение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает ввод с клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP
            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT
            game_object.update_direction()
            game_object.move()


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Создание экземпляров классов
    apple = Apple()
    snake = Snake(apple)
    apple.draw()
    while True:
        # Задание скорости игры
        clock.tick(SPEED)
        # Управление змейкой
        handle_keys(snake)
        # Отрисовка нового яблока, если старое съедено
        if len(snake.positions) > snake.length:
            apple.draw()
            snake.length += 1
        # Отрисовка змейки
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
