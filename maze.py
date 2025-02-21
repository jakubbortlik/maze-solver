import random
import time
from typing import Iterable
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
        self._break_walls_r(random.randrange(num_rows), random.randrange(num_cols))
        self._reset_cells_visited()

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

    def solve(self) -> bool:
        """Return True if the maze was solved, False otherwise."""
        return self._solve_r(0, 0)

    def _draw_cell(self, i, j, sleep=0.01):
        self._cells[i][j].draw()
        self._animate(sleep)

    def _animate(self, sleep=0.01):
        if self.win is not None:
            self.win.redraw()
        time.sleep(sleep)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(-1, -1)
    
    def _get_neighbor_opts(self, i, j) -> Iterable[tuple[int, int, str, str]]:
        """Yield possible neighbors of a cell."""
        if i > 0:
            yield (i-1, j, "right", "left")
        if i < self.num_rows - 1:
            yield (i+1, j, "left", "right")
        if j > 0:
            yield (i, j-1, "bottom", "top")
        if j < self.num_cols - 1:
            yield (i, j+1, "top", "bottom")

    def _get_visitable_neighbors(self, i, j) -> Iterable[tuple[int, int]]:
        """Yield neighbors of cell where there's no wall between the two."""
        if i > 0 and not self._cells[i-1][j].has_right_wall:
            yield (i-1, j)
        if i < self.num_rows - 1 and not self._cells[i+1][j].has_left_wall:
            yield (i+1, j)
        if j > 0 and not self._cells[i][j-1].has_bottom_wall:
            yield (i, j-1)
        if j < self.num_cols - 1 and not self._cells[i][j+1].has_top_wall:
            yield (i, j+1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            for neighbor_opts in self._get_neighbor_opts(i, j):
                neighbor = self._cells[neighbor_opts[0]][neighbor_opts[1]]
                if not neighbor.visited:
                    to_visit.append(neighbor_opts)
            if len(to_visit) == 0:
                self._draw_cell(i, j, sleep=0.01)
                return
            _i, _j, neighbor_wall, my_wall = random.choice(to_visit)
            setattr(self._cells[_i][_j], f"has_{neighbor_wall}_wall", False)
            setattr(self._cells[i][j], f"has_{my_wall}_wall", False)
            self._draw_cell(_i, _j, sleep=0.01)
            self._break_walls_r(_i, _j)

    def _reset_cells_visited(self) -> None:
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def _solve_r(self, i: int, j: int):
        """Return True if the cell leads to solving the maze."""
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        while True:
            for neighbor_coordinates in self._get_visitable_neighbors(i, j):
                neighbor = self._cells[neighbor_coordinates[0]][neighbor_coordinates[1]]
                if not neighbor.visited:
                    self._cells[i][j].draw_move(neighbor)
                    solves_maze = self._solve_r(*neighbor_coordinates)
                    if solves_maze:
                        return True
                    self._cells[i][j].draw_move(neighbor, undo=True)
            self._animate()
            return False
