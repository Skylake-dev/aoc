from copy import deepcopy

with open('./input') as data:
    # input is a single line
    input = data.readline()

program: list[int] = list(map(int, input.split(',')))

class IntCodeComputer:
    def __init__(self, program: list[int]) -> None:
        # copy the program to memory
        self.program = deepcopy(program)
        # program counter to keep track of index
        self.pc: int = 0
        # current operation and registers
        self.current_opcode: int = 0
        self.op1_address: int = 0
        self.op2_address: int = 0
        self.dest_address: int = 0
        # True until program is running, i.e.
        # when opcode is not 99
        self.running = True

    def _fetch(self) -> None:
        self.current_opcode = self.program[self.pc]
        if self.current_opcode == 99:
            self.running = False
            return
        self.op1_address = self.program[self.pc+1]
        self.op2_address = self.program[self.pc+2]
        self.dest_address = self.program[self.pc+3]

    def _do_operation(self) -> None:
        # get operand values
        op1 = self.program[self.op1_address]
        op2 = self.program[self.op2_address]
        # check opcode to do correct operation
        if self.current_opcode == 1:
            result = op1 + op2
        elif self.current_opcode == 2:
            result = op1 * op2
        else:
            raise RuntimeError('invalid opcode')
        # store result at correct position
        self.program[self.dest_address] = result

    def _next(self) -> None:
        self.pc += 4

    def set_program(self, program: list[int]) -> None:
        self.program = deepcopy(program)
        self.running = True
        self.pc = 0

    def run(self) -> None:
        self._fetch()
        while(self.running):
            self._do_operation()
            self._next()
            self._fetch()

###############
# part 1
###############

computer = IntCodeComputer(program)
computer.program[1] = 12
computer.program[2] = 2
computer.run()

print(f'part 1: {computer.program[0]}')

###############
# part 2
###############

target = 19690720
found = False
solutions = (0, 0)
for noun in range(0, 100):
    if found:
        break
    for verb in range(0, 100):
        computer.set_program(program)
        computer.program[1] = noun
        computer.program[2] = verb
        computer.run()
        if computer.program[0] == target:
            solutions = (noun, verb)
            break

print(f'part 2: {100 * solutions[0] + solutions[1]}')