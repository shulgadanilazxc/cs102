import argparse
import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        for j in range(self.life.cols + 2):
            screen.addstr(0, j, "-")

        for i in range(self.life.rows + 2):
            screen.addstr(i, 0, "|")
            screen.addstr(i, self.life.cols + 1, "|")

        for j in range(self.life.cols + 2):
            screen.addstr(self.life.rows + 1, j, "-")

        screen.refresh()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, "+")

        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()

        curses.cbreak()
        curses.noecho()
        screen.nodelay(True)

        screen.clear()
        screen.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        k = 0
        running = True
        while running:
            if (
                self.life.is_changing is False
                or self.life.is_max_generations_exceeded is True
            ):
                running = False

            screen.clear()
            height, width = screen.getmaxyx()

            self.draw_borders(screen)

            self.draw_grid(screen)
            self.life.step()

            k = screen.getch()
            if k == ord("q"):
                running = False
            statusbarstr = f"Press 'q' to exit | Life console"
            statusbarstr += "" if running else " | WAITING FOR QUIT..."

            screen.attron(curses.color_pair(1))
            screen.addstr(height - 1, 0, statusbarstr)
            screen.addstr(
                height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1)
            )
            screen.attroff(curses.color_pair(3))

            screen.refresh()
            curses.napms(1000)

        curses.endwin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10, help="Количество строк")
    parser.add_argument("--columns", type=int, default=10, help="Количество столбцов")
    parser.add_argument(
        "--max_generations",
        type=float,
        default=float("inf"),
        help="Максимальное число поколений",
    )

    args = parser.parse_args()

    life = GameOfLife(
        size=(args.rows, args.columns), max_generations=args.max_generations
    )

    instance = Console(life)
    instance.run()
