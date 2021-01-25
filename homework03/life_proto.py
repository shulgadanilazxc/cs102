import copy
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(True)

        self.draw_lines()

        self.draw_grid()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_grid()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = list(self.get_next_generation())

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        matrix = []

        for y in range(self.cell_height):

            row = []
            for x in range(self.cell_width):
                if randomize is True:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)

            matrix.append(row)

        return matrix

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = 0
        x = 0

        for i in range(self.cell_height):

            x = 0

            for j in range(self.cell_width):

                if self.grid[i][j] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1),
                    )

                x += self.cell_size

            y += self.cell_size

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neigbours = []

        start_row = None
        end_row = None
        start_column = None
        end_column = None

        if cell[0] == 0:
            start_row = cell[0]
        else:
            start_row = cell[0] - 1

        if cell[0] == self.cell_height - 1:
            end_row = cell[0]
        else:
            end_row = cell[0] + 1

        if cell[1] == 0:
            start_column = cell[1]
        else:
            start_column = cell[1] - 1

        if cell[1] == self.cell_width - 1:
            end_column = cell[1]
        else:
            end_column = cell[1] + 1

        for i in range(start_row, end_row + 1):
            for j in range(start_column, end_column + 1):
                if i != cell[0] or j != cell[1]:
                    neigbours.append(self.grid[i][j])

        return neigbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        next = [[0 for j in range(self.cell_width)] for i in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):

                neighbours = self.get_neighbours((i, j))

                if sum(neighbours) < 2:
                    next[i][j] = 0

                elif sum(neighbours) > 3:
                    next[i][j] = 0

                elif sum(neighbours) == 3:
                    next[i][j] = 1

                else:
                    next[i][j] = self.grid[i][j]

        return next


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
