from __future__ import annotations
from typing import Any, Callable, Dict

MISSING: Any = None


class Node:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0
        self.next: Node = MISSING
        self.move: Dict[str, Callable] = {
            'U': self._move_up,
            'D': self._move_down,
            'R': self._move_right,
            'L': self._move_left
        }

    def _move_up(self) -> None:
        self.y += 1

    def _move_down(self) -> None:
        self.y -= 1

    def _move_right(self) -> None:
        self.x += 1

    def _move_left(self) -> None:
        self.x -= 1

    def _follow_x(self, prev: Node) -> None:
        if self.x > prev.x:
            self.x -= 1
        else:
            self.x += 1

    def _follow_y(self, prev: Node) -> None:
        if self.y > prev.y:
            self.y -= 1
        else:
            self.y += 1

    def follow(self, prev: Node) -> None:
        if self.x == prev.x:
            # can only follow on y
            if self.y == prev.y or abs(self.y - prev.y) == 1:
                return
            self._follow_y(prev)
        elif self.y == prev.y:
            # can only follow on x
            if self.x == prev.x or abs(self.x - prev.x) == 1:
                return
            self._follow_x(prev)
        else:
            # can only follow diagonally
            if abs(self.y - prev.y) == 1 and abs(self.x - prev.x) == 1:
                return
            self._follow_x(prev)
            self._follow_y(prev)
