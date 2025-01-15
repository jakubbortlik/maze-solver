from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2
        )


class Window:
    def __init__(self, width, height, bg="black"):
        self.__root = Tk()
        self.__root.title = "Maze solver"
        self.__canvas = Canvas(self.__root, bg=bg, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self._bg = bg

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


class Cell:
    def __init__(
        self,
        x1,
        x2,
        y1,
        y2,
        win: Window | None = None,
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bottom_wall: bool = True,
        color: str = "pink",
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.color = color
        self.visited = False

    def draw(self):
        if self._win is not None:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            color = self.color if self.has_left_wall else self._win._bg
            self._win.draw_line(line, color)

            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            color = self.color if self.has_right_wall else self._win._bg
            self._win.draw_line(line, color)

            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            color = self.color if self.has_top_wall else self._win._bg
            self._win.draw_line(line, color)

            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            color = self.color if self.has_bottom_wall else self._win._bg
            self._win.draw_line(line, color)

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        line = Line(
            Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2),
            Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2),
        )
        if self._win is not None:
            self._win.draw_line(line, color)
