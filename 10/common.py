from enum import Enum
from typing import Any, List, Generator

MISSING: Any = None


class Opcode(Enum):
    ADDX = 'addx'
    NOOP = 'noop'


class Pixel(Enum):
    LIT = '#'
    DARK = '.'


class Clock:
    def __init__(self) -> None:
        # cycle that is currently running
        self.current_cycle: int = 0
        self.stop: bool = False

    def tick(self) -> Generator[int, None, None]:
        while (not self.stop):
            self.current_cycle += 1
            yield self.current_cycle


class Instruction:
    def __init__(self, line: str) -> None:
        line = line.strip(' \n')
        self.opcode: Opcode = Opcode(line[0:4])
        if self.opcode is Opcode.ADDX:
            self.argument: int = int(line.split(' ')[1])
            self.clocks_required: int = 2
        else:
            self.argument = 0
            self.clocks_required = 1
        self._elapsed_clock: int = 0
        self.completed: bool = False

    def cycle(self, X: int) -> int:
        self._elapsed_clock += 1
        if self._elapsed_clock == self.clocks_required:
            self.completed = True
            return self.apply_effect(X)
        return X

    def apply_effect(self, X: int) -> int:
        if self.opcode is Opcode.ADDX:
            return X + self.argument
        else:
            return X


class CPU:
    def __init__(self, clock: Clock, program: List[Instruction]) -> None:
        self.clock: Clock = clock
        self.program: List[Instruction] = program
        self.X: int = 1             # value of X during current cycle
        self.X_next: int = self.X   # value that X will have in the next cycle
        self.current_instruction: Instruction = program.pop(0)

    def cycle(self):
        self.X = self.X_next
        if self.current_instruction.completed:
            try:
                self.current_instruction = self.program.pop(0)
            except IndexError:
                self.clock.stop = True
                return
        self.X_next = self.current_instruction.cycle(self.X)


class CRT:
    def __init__(self, clock: Clock) -> None:
        self.clock: Clock = clock
        self.size: int = 240
        self.pixels: List[Pixel] = []
        for i in range(self.size):
            self.pixels.append(Pixel.DARK)

    def __str__(self) -> str:
        string = ''
        for i, pixel in enumerate(self.pixels):
            if i % 40 == 0:
                string += '\n'
            string += pixel.value
        return string

    def cycle(self, pos: int) -> None:
        if self.sprite_visible(pos):
            self.pixels[self.clock.current_cycle - 1] = Pixel.LIT

    def sprite_visible(self, pos: int) -> bool:
        sprite = (pos - 1, pos, pos + 1)
        if ((self.clock.current_cycle - 1) % 40) in sprite:
            return True
        return False
