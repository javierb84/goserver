from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        # Create root window
        self.__root = Tk()
        self.__root.title("Graphical Window")

        # Optional: make the window background white too
        self.__root.configure(bg="white")

        # Running state
        self.running = False

        # Create canvas with white background
        self.canvas = Canvas(
            self.__root,
            width=width,
            height=height,
            bg="white",
        )

        self.canvas.pack(fill=BOTH, expand=True)

        # Handle window close button
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True

        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )


def main():
    from maze import Maze

    win = Window(800, 600)

    maze = Maze(
        x1=50,
        y1=50,
        num_rows=10,
        num_cols=10,
        cell_size_x=40,
        cell_size_y=40,
        win=win,
        seed=0,
    )

    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
