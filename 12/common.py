from __future__ import annotations
import io
from typing import Any, Dict, Generator, List, NamedTuple, Optional


MISSING: Any = None
levels = 'abcdefghijklmnopqrstuvwxyz'
heights: Dict[str, int] = {}
for i, letter in enumerate(levels):
    heights[letter] = i


class Cell:
    def __init__(self, height: int) -> None:
        self.height: int = height
        self.visited: bool = False
        self.neighbours: Neighbours

    def can_climb_to(self, other: Optional[Cell]) -> bool:
        if not other:
            return False
        return self.height >= (other.height - 1)


class Neighbours(NamedTuple):
    up: Optional[Cell]
    down: Optional[Cell]
    left: Optional[Cell]
    right: Optional[Cell]


class Heatmap:
    def __init__(self, data: io.TextIOWrapper) -> None:
        self.heatmap: List[List[Cell]] = []
        self.start: Cell = MISSING
        self.end: Cell = MISSING
        self._parse_input(data)

    def _parse_input(self, data: io.TextIOWrapper) -> None:
        for i, line in enumerate(data):
            self.heatmap.append([])
            for char in line.strip():
                if char in heights:
                    self.heatmap[i].append(Cell(heights[char]))
                elif char == 'S':
                    start = Cell(heights['a'])
                    self.heatmap[i].append(start)
                    self.start = start
                else:
                    end = Cell(heights['z'])
                    self.heatmap[i].append(end)
                    self.end = end
        self._make_connections()

    def _get_neighbours(self, x: int, y: int) -> Neighbours:
        Neighbours(up=None, down=None, left=None, right=None)
        cell = self.heatmap[x][y]
        if x != 0 and cell.can_climb_to(self.heatmap[x-1][y]):
            up = self.heatmap[x-1][y]
        else:
            up = None
        if x != (len(self.heatmap) - 1) and cell.can_climb_to(self.heatmap[x+1][y]):
            down = self.heatmap[x+1][y]
        else:
            down = None
        if y != 0 and cell.can_climb_to(self.heatmap[x][y-1]):
            left = self.heatmap[x][y-1]
        else:
            left = None
        if y != (len(self.heatmap[x]) - 1) and cell.can_climb_to(self.heatmap[x][y+1]):
            right = self.heatmap[x][y+1]
        else:
            right = None
        return Neighbours(up=up, down=down, left=left, right=right)

    def _make_connections(self) -> None:
        for x, row in enumerate(self.heatmap):
            for y, cell in enumerate(row):
                cell.neighbours = self._get_neighbours(x, y)

    def reset_visits(self) -> None:
        for row in self.heatmap:
            for cell in row:
                cell.visited = False

    def iterate(self) -> Generator[Cell, None, None]:
        for row in self.heatmap:
            for cell in row:
                yield cell


def shortest_path(heatmap: Heatmap, start: Cell, end: Cell) -> List[Cell]:
    path_list = [[start]]
    path_index = 0
    start.visited = True
    if start == end:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = last_node.neighbours
        # end of path
        if end in next_nodes:
            current_path.append(end)
            return current_path
        # explore new paths
        for next_node in next_nodes:
            if next_node is not None and not next_node.visited:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                next_node.visited = True
        # continue to next path in list
        path_index += 1
    # no path is found
    return []


def print_path(path: List[Cell]):
    print([cell.height for cell in path])
