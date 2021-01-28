import argparse

import pygame

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self,
        life: GameOfLife,
        cell_size: int = 10,
        width: int = 600,
        height: int = 600,
        speed: int = 10,
    ) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.screen_size = width + 2, height + 2
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        width = self.screen_size[0]
        height = self.screen_size[1]

        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = 0

        for i in range(self.life.rows):

            x = 0

            cell_size = self.cell_size

            for j in range(self.life.cols):

                if self.life.curr_generation[i][j] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x + 1, y + 1, cell_size - 1, cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x + 1, y + 1, cell_size - 1, cell_size - 1),
                    )

                x += cell_size

            y += cell_size

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.life.curr_generation = self.life.create_grid(True)

        self.draw_lines()

        self.draw_grid()

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause:
                        x, y = event.pos
                        cell_x, cell_y = x // self.cell_size, y // self.cell_size

                        self.life.curr_generation[cell_y][cell_x] = abs(
                            self.life.curr_generation[cell_y][cell_x] - 1
                        )
                elif (
                    self.life.is_changing is False
                    or self.life.is_max_generations_exceeded is True
                ):
                    running = False

            self.draw_grid()

            if pause is False:
                self.life.step()

            pygame.display.flip()

            if pause:
                clock.tick(30)
            else:
                clock.tick(1)
        pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    default_grid_width = 10
    default_grid_height = 10
    default_width = 600
    default_height = 600
    default_cell_size = int(
        min(default_width, default_height)
        / max(default_grid_width, default_grid_height)
    )

    parser.add_argument(
        "--grid_width",
        type=int,
        default=default_grid_width,
        help="Ширина игрового поля в клетках",
    )
    parser.add_argument(
        "--grid_height",
        type=int,
        default=default_grid_height,
        help="Высота игрового поля в клетках",
    )
    parser.add_argument("--width", type=int, default=default_width, help="Ширина окна")
    parser.add_argument(
        "--height", type=int, default=default_height, help="Высота окна"
    )
    parser.add_argument(
        "--cell_size", type=int, default=default_cell_size, help="Размер одной ячейки"
    )

    args = parser.parse_args()

    life = GameOfLife(size=(args.grid_height, args.grid_width))
    instance = GUI(life, cell_size=args.cell_size, width=args.width, height=args.height)
    instance.run()
