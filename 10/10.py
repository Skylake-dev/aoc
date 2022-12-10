from common import (
    Clock,
    Instruction,
    CPU,
    CRT
)
from typing import List

program: List[Instruction] = []

with open('./input') as data:
    for line in data:
        program.append(Instruction(line))

clock = Clock()
cpu = CPU(clock, program)
crt = CRT(clock)

signal_strengths: List[int] = []

for cycle in clock.tick():
    cpu.cycle()
    crt.cycle(cpu.X)
    if cycle == 20 or (cycle - 20) % 40 == 0:
        signal_strengths.append(cycle * cpu.X)

print(f'Total strength = {sum(signal_strengths)}')
print(f'part 2{str(crt)}')
