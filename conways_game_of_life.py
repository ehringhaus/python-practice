'''
CONWAY'S GAME OF LIFE
A world is made with m rows, n cols
Each cell is either dead or alive, initially random
In each generation (a loop of the draw function), cells are either killed or resurrected.

HELPFUL LINKS
Peter Norvig:
https://nbviewer.jupyter.org/url/norvig.com/ipython/Life.ipynb
'''

from helpers import coroutine, compose

# other
from p5 import *
from dataclasses import dataclass, field
from typing import List
from random import random
from itertools import product


@dataclass(frozen=True)
class Window:
    size: tuple = (750, 750)
    title: str = 'Conway\'s Game of Life'
    bg_color: int = 255


@dataclass
class World:
    rows: int = 12
    cols: int = 12
    bg_color: int = 255
    p: float = 0.33
    cells: set = field(default_factory=set)


@ dataclass
class Cell:
    pos: tuple
    shape: str = 'rect'
    mode: str = 'CORNER'
    color: int = 0
    size: tuple = field(init=False)
    shape_func: str = field(init=False)
    scaled_x: int = field(init=False)
    scaled_y: int = field(init=False)
    p: float = field(init=False)
    alive: bool = field(init=False)
    neighborhood: List[tuple] = field(default_factory=list)
    neighbors: int = 0

    def __post_init__(self):
        self.size: tuple = (width / World.rows, height / World.cols)
        shape_width, shape_height = self.size
        self.scaled_x = int(self.pos[0] * shape_width)
        self.scaled_y = int(self.pos[1] * shape_height)
        self.shape_func: str = f'{self.shape}({self.scaled_x, self.scaled_y}, {shape_width}, {shape_height}, mode=\'{self.mode}\')'

        self.p: float = random()
        self.alive: bool = True if self.p < World.p else False

        x, y = self.pos
        steps = list(product((-1, 0, 1), repeat=2))
        steps.remove((0, 0))
        self.neighborhood = [(x + sx, y + sy)
                             for (sx, sy) in steps if (x + sx >= 0) and
                                                      (y + sy) >= 0 and
                                                      (x + sx < World.rows) and
                                                      (y + sy < World.cols)]


def generate_coords(cor):
    for row in range(World.rows):
        for col in range(World.cols):
            coords = (row, col)
            cor.send(coords)


@coroutine
def spawn_cell(cor):
    while True:
        coords = (yield)
        cell = Cell(pos=(coords))
        cor.send((coords, cell))


@coroutine
def save_cell():
    while True:
        coords, cell = (yield)
        cells[(coords)] = cell


def draw_cell(cell):
    if cell.alive:
        fill(cell.color)
        eval(cell.shape_func)


def transmit_livelihood(cell):
    if cell.alive:
        for pos in cell.neighborhood:
            cells[(pos)].neighbors += 1


def next_generation(cell):
    if cell.alive is False and (cell.neighbors == 3):
        cell.alive = True
    elif cell.alive is True and (cell.neighbors == 2) or (cell.neighbors == 3):
        cell.alive = True
    else:
        cell.alive = False
    cell.neighbors = 0


cells = {}


def setup():
    size(*Window.size)
    title(Window.title)

    cell = save_cell()
    pipeline = compose(generate_coords, spawn_cell)
    pipeline(cell)


def draw():
    background(Window.bg_color)

    for cell in cells.values():
        draw_cell(cell)
        transmit_livelihood(cell)
        next_generation(cell)


if __name__ == '__main__':
    run(frame_rate=7)
