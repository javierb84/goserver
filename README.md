This program creates a window, draws a grid of rooms, randomly knocks down walls to build a maze, and then uses a recursive search algorithm to find a path from the entrance to the exit while showing every step visually.



Imagine this program as a robot that builds a maze on a piece of paper and then solves it while you watch.

There are two main files:

graphics.py → the paper, pencil, and window on the screen
maze.py → the brain that builds and solves the maze
Part 1: graphics.py — The Drawing Tools

This file doesn't know anything about mazes. Its job is simply to create a window and draw lines.

Window

Think of the Window class as opening a blank sheet of paper.

win = Window(800, 600)

means:

"Open a window that is 800 pixels wide and 600 pixels tall."

Inside that window is a canvas.

A canvas is like a whiteboard where we can draw.

Point

A Point is just a location.

Point(100, 50)

means:

A spot that is 100 pixels from the left and 50 pixels from the top.

Like a coordinate on graph paper.

Line

A line connects two points.

Line(
    Point(0, 0),
    Point(100, 0)
)

means:

Draw a line from the upper-left corner to a point 100 pixels to the right.

draw_line()

When the maze wants to draw something:

window.draw_line(...)

the Window tells the Canvas:

"Draw this line on the screen."

redraw()

Computers don't automatically repaint graphics.

The redraw method tells the window:

"Show everything that has been drawn so far."

Without it, nothing would appear until the very end.

wait_for_close()

This method keeps the window alive.

Without it:

Window opens
Window immediately closes

which would be annoying.

Instead it repeatedly checks:

"Has the user closed the window yet?"

If not, keep running.

Part 2: maze.py — Building the Maze

This file contains all the maze logic.

Cell

A maze is made of many square rooms.

Each room is a Cell.

Imagine one square:

+---+
|   |
+---+

A cell keeps track of four walls:

has_left_wall
has_right_wall
has_top_wall
has_bottom_wall

Each wall is either:

True

meaning:

wall exists

or

False

meaning:

wall removed

Cell.draw()

This draws the square.

For each wall:

if wall exists:
    draw line

So the cell decides:

Should I draw my left wall?

Should I draw my right wall?

etc.

Cell.draw_move()

This draws the red solving path.

Imagine the solver walking:

A --> B

The method:

Finds the center of Cell A
Finds the center of Cell B
Draws a line connecting them

Red means:

I'm exploring here

Gray means:

Dead end. Backtracking.

Maze

The Maze class is the entire maze.

Think of it as a big collection of cells.

Creating the Maze

When you create:

Maze(...)

the constructor runs.

It does several things.

Step 1: Create all cells
self.__create_cells()

Creates a grid.

For example:

□ □ □
□ □ □
□ □ □

Every square starts with all four walls.

Step 2: Break walls
self.__break_walls_r(0,0)

This turns the grid into a maze.

Step 3: Open entrance and exit

The first cell gets an opening:

Entrance
   ↓
+   +
|   |
+---+

The last cell gets an exit.

Step 4: Reset visited

During maze creation every cell becomes:

visited = True

We clear that so the solver can reuse it later.

How Maze Generation Works

This is the coolest part.

The algorithm starts in the upper-left corner.

S □ □
□ □ □
□ □ □

It marks the starting cell:

visited = True

Then it looks around.

Possible moves:

→ right
↓ down

Choose one randomly.

Suppose it chooses right.

It knocks down the wall:

Before:

|A|B|

After:

|A B|

Now it moves into B.

Again:

Mark visited
Pick a random neighbor
Knock down a wall
Move there

Repeat forever.

Eventually it gets stuck.

No unvisited neighbors remain.

At that point it goes backward.

This is called:

backtracking

Eventually every cell gets visited.

Result:

A complete maze

with one connected path between all rooms.

What Does "seed=0" Do?

Computers aren't truly random.

A seed controls the sequence.

If:

seed=0

you always get:

same maze
same maze
same maze

every run.

Great for debugging.

Without a seed:

different maze
different maze
different maze

every run.

Solving the Maze

After generation:

maze.solve()

runs.

The solver starts at:

upper-left corner

Goal:

lower-right corner
_solve_r()

This is another recursive algorithm.

At each cell:

Mark visited
Check if we're at the goal
Try moving right
Try moving left
Try moving down
Try moving up

Suppose it goes the wrong way.

Start
  |
  v
Dead End

The recursive call returns:

False

meaning:

This path doesn't work.

Then:

draw_move(..., undo=True)

draws a gray line.

That tells you:

We tried this path and it failed.

Eventually a path reaches the exit.

Then:

return True

which ripples all the way back up the recursive calls.

The solver stops.

What You See On Screen

When you run the program:

Phase 1

A grid appears.

□ □ □ □
□ □ □ □
□ □ □ □
Phase 2

Walls disappear.

Maze generation

You watch the maze being carved out.

Phase 3

The solver begins.

Red lines:

Searching

Gray lines:

Wrong path
Backtracking
Phase 4

The red path reaches the exit.

The maze is solved.
