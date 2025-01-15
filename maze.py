import random
import time
from graphics import Cell, Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
        seed: int | None = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)
        self.create_cells()
        self._break_entrance_and_exit()

    def create_cells(self):
        self._cells = []
        for col in range(self.num_cols):
            rows = []
            for row in range(self.num_rows):
                rows.append(
                    Cell(
                        self.x1 + col * self.cell_size_x,
                        self.x1 + (col + 1) * self.cell_size_x,
                        self.y1 + row * self.cell_size_y,
                        self.y1 + (row + 1) * self.cell_size_y,
                        self.win,
                    )
                )
            self._cells.append(rows)
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self.win is not None:
            self.win.redraw()
            time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(-1, -1)


def main():
    win = Window(800, 600)
    Maze(100, 100, 10, 10, 50, 50, win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
