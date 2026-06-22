import random
import time

from graphics import Point, Line


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.visited = False

        self.__x1 = -1.0
        self.__y1 = -1.0
        self.__x2 = -1.0
        self.__y2 = -1.0

        self.__win = win

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win is None:
            return

        # Left wall
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")

        # Top wall
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")

        # Right wall
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
        else:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")

        # Bottom wall
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
        else:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        if self.__win is None:
            return

        from_center_x = (self.__x1 + self.__x2) / 2
        from_center_y = (self.__y1 + self.__y2) / 2

        to_center_x = (to_cell._Cell__x1 + to_cell._Cell__x2) / 2
        to_center_y = (to_cell._Cell__y1 + to_cell._Cell__y2) / 2

        color = "blue" if undo else "red"

        self.__win.draw_line(
            Line(
                Point(from_center_x, from_center_y),
                Point(to_center_x, to_center_y),
            ),
            color,
        )


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win=None,
        seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)

        self.__cells = []

        self.__create_cells()

        self.__break_walls_r(0, 0)

        # Entrance and exit
        self.__cells[0][0].has_top_wall = False
        self.__cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False

        self.__draw_cell(0, 0)
        self.__draw_cell(
            self._num_cols - 1,
            self._num_rows - 1,
        )

        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self._num_cols):
            col = []

            for j in range(self._num_rows):
                col.append(Cell(self._win))

            self.__cells.append(col)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self.__cells[i][j].draw(
            x1,
            y1,
            x2,
            y2,
        )

        self.__animate()

    def __animate(self):
        if self._win is None:
            return
        self._win.redraw()
        # Sleep less so generation is fast, or only sleep during solve!
        time.sleep(0.01) 

    def __break_walls_r(self, i, j):
        current = self.__cells[i][j]
        current.visited = True

        while True:
            to_visit = []

            # Right
            if (
                i + 1 < self._num_cols
                and not self.__cells[i + 1][j].visited
            ):
                to_visit.append((i + 1, j))

            # Left
            if (
                i - 1 >= 0
                and not self.__cells[i - 1][j].visited
            ):
                to_visit.append((i - 1, j))

            # Down
            if (
                j + 1 < self._num_rows
                and not self.__cells[i][j + 1].visited
            ):
                to_visit.append((i, j + 1))

            # Up
            if (
                j - 1 >= 0
                and not self.__cells[i][j - 1].visited
            ):
                to_visit.append((i, j - 1))

            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return

            next_i, next_j = random.choice(to_visit)
            next_cell = self.__cells[next_i][next_j]

            if next_i == i + 1:
                current.has_right_wall = False
                next_cell.has_left_wall = False

            elif next_i == i - 1:
                current.has_left_wall = False
                next_cell.has_right_wall = False

            elif next_j == j + 1:
                current.has_bottom_wall = False
                next_cell.has_top_wall = False

            elif next_j == j - 1:
                current.has_top_wall = False
                next_cell.has_bottom_wall = False

            self.__draw_cell(i, j)
            self.__draw_cell(next_i, next_j)

            self.__break_walls_r(next_i, next_j)

    def __reset_cells_visited(self):
        for column in self.__cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self.__animate()

        current = self.__cells[i][j]
        current.visited = True

        if (
            i == self._num_cols - 1
            and j == self._num_rows - 1
        ):
            return True

        # Right
        if (
            i + 1 < self._num_cols
            and not current.has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            next_cell = self.__cells[i + 1][j]
            current.draw_move(next_cell)

            if self._solve_r(i + 1, j):
                return True

            current.draw_move(next_cell, True)

        # Left
        if (
            i - 1 >= 0
            and not current.has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            next_cell = self.__cells[i - 1][j]
            current.draw_move(next_cell)

            if self._solve_r(i - 1, j):
                return True

            current.draw_move(next_cell, True)

        # Down
        if (
            j + 1 < self._num_rows
            and not current.has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            next_cell = self.__cells[i][j + 1]
            current.draw_move(next_cell)

            if self._solve_r(i, j + 1):
                return True

            current.draw_move(next_cell, True)

        # Up
        if (
            j - 1 >= 0
            and not current.has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            next_cell = self.__cells[i][j - 1]
            current.draw_move(next_cell)

            if self._solve_r(i, j - 1):
                return True

            current.draw_move(next_cell, True)

        return False
