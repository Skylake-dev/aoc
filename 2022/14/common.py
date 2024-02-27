from enum import Enum
from io import TextIOWrapper
import time
from typing import Any, Generator, List, Optional, Tuple

MISSING: Any = None


class Material(Enum):
    SAND = 'sand'
    ROCK = 'rock'
    AIR = 'air'


class Cell:
    def __init__(self, x: int, y: int, material: Material = MISSING) -> None:
        self.x: int = x
        self.y: int = y
        self.material: Material = material
        self.down: Optional[Cell] = None
        self.down_left: Optional[Cell] = None
        self.down_right: Optional[Cell] = None

    def can_go_down(self) -> bool:
        if not self.down:
            return False
        if self.down.material in (Material.ROCK, Material.SAND):
            return False
        return True

    def can_go_down_left(self) -> bool:
        if not self.down_left:
            return False
        if self.down_left.material in (Material.ROCK, Material.SAND):
            return False
        return True

    def can_go_down_right(self) -> bool:
        if not self.down_right:
            return False
        if self.down_right.material in (Material.ROCK, Material.SAND):
            return False
        return True


class Cave:
    def __init__(self, data: TextIOWrapper) -> None:
        self.width = 700
        self.cave: List[List[Cell]] = []
        for x in range(self.width):
            self.cave.append([])
            for y in range(200):
                self.cave[x].append(Cell(x, y, Material.AIR))
        self.sand_spawn_point: Cell = self.get_cell(500, 0)
        assert self.sand_spawn_point.x == 500 and self.sand_spawn_point.y == 0
        self.max_depth: int = 0
        self.max_depth_reached: bool = False
        self.spawn_reached: bool = False
        self._parse_cave(data)
        self._compute_paths()

    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self.width and 0 <= y < 200:
            return self.cave[x][y]
        raise IndexError

    def _parse_cave(self, data: TextIOWrapper) -> None:
        for line in data:
            walls = line.strip().split(' -> ')
            for i in range(len(walls) - 1):
                j = i+1
                self._draw_wall(walls[i], walls[j])

    def _draw_wall(self, start: str, end: str) -> None:
        start_x, start_y = start.split(',', 2)
        end_x, end_y = end.split(',', 2)
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        self._update_borders(start_y, end_y)
        if start_x == end_x:
            self._draw_vertical(start_x,  start_y, end_x, end_y)
        elif start_y == end_y:
            self._draw_horizontal(start_x, start_y, end_x, end_y)

    def _draw_vertical(self, start_x: int, start_y: int, end_x: int, end_y: int):
        sign = 1
        length = end_y - start_y
        if length < 0:
            sign = -1
            length = -length
        length += 1
        for i in range(length):
            cell = self.get_cell(start_x, start_y+(i*sign))
            cell.material = Material.ROCK

    def _draw_horizontal(self, start_x: int, start_y: int, end_x: int, end_y: int):
        sign = 1
        length = end_x - start_x
        if length < 0:
            sign = -1
            length = -length
        length += 1
        for i in range(length):
            cell = self.get_cell(start_x+(i*sign), start_y)
            cell.material = Material.ROCK

    def _update_borders(self, y1, y2) -> None:
        if self.max_depth < y1:
            self.max_depth = y1
        elif self.max_depth < y2:
            self.max_depth = y2

    def _compute_paths(self) -> None:
        for x, y, cell in self.iterate():
            try:
                down_cell = self.get_cell(x, y+1)
            except IndexError:
                cell.down = None
            else:
                cell.down = down_cell
            try:
                down_left_cell = self.get_cell(x-1, y+1)
            except IndexError:
                cell.down_left = None
            else:
                cell.down_left = down_left_cell
            try:
                down_right_cell = self.get_cell(x+1, y+1)
            except IndexError:
                cell.down_right = None
            else:
                cell.down_right = down_right_cell

    def iterate(self) -> Generator[Tuple[int, int, Cell], None, None]:
        for row in self.cave:
            for cell in row:
                yield (cell.x, cell.y, cell)

    def sand_fall(self, cell: Cell) -> None:
        if cell.can_go_down():
            next_cell = cell.down
        elif cell.can_go_down_left():
            next_cell = cell.down_left
        elif cell.can_go_down_right():
            next_cell = cell.down_right
        else:
            next_cell = None
        if next_cell:
            # print(f'next cell {next_cell.x}, {next_cell.y}')
            if next_cell.y > self.max_depth:
                self.max_depth_reached = True
            else:
                self.sand_fall(next_cell)
        else:
            cell.material = Material.SAND
            if cell == self.sand_spawn_point:
                self.spawn_reached = True

    def print_cave(self) -> None:
        cave = ''
        for y in range(self.max_depth+5):
            cave += '\n'
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.material == Material.ROCK:
                    cave += '#'
                elif cell.material == Material.SAND:
                    cave += 'o'
                else:
                    cave += '.'
        print(f'{cave}\nMax depth = {self.max_depth}')

    def remove_sand(self) -> None:
        for x, y, cell in self.iterate():
            if cell.material is Material.SAND:
                cell.material = Material.AIR
        self.max_depth_reached = False

    def add_bottom(self) -> None:
        self.max_depth += 2
        for x in range(self.width):
            cell = self.get_cell(x, self.max_depth)
            cell.material = Material.ROCK
