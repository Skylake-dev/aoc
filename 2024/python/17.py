import re
from math import floor
from time import time
# use collections instead of deprecated typing
from collections.abc import Callable

with open('../inputs/17.txt') as data:
    input = data.readlines()

###############
# input parsing
###############

assert len(input) == 5
# regex to parse integers from the line
integer = r'[0-9]+'
integer = re.compile(integer)


def get_int(line) -> int:
    # helper to check None
    m = re.search(integer, line)
    assert m is not None
    return int(m[0])


# get the registers and program from the input file
reg_a = int(get_int(input[0]))
reg_b = int(get_int(input[1]))
reg_c = int(get_int(input[2]))
# empty line
program = list(map(int, re.findall(integer, input[4])))

###############
# utils
###############


class ThreeBitComputer:
    """Keeps track of the state of the 3 bit computer used
    to parse the program
    """

    def __init__(self, a: int, b: int, c: int, program: list[int]) -> None:
        self.reg_a = a
        self.reg_b = b
        self.reg_c = c
        self.program = program
        # store result of out instructions
        self.out: list[int] = []
        # stores the current instruction pointer
        self.ip: int = 0
        # state of the computation
        self.curr_opcode: int = 0
        self.curr_operand: int = 0
        # decoded operand value according to the instruction
        self.operand_value: int = 0
        # map opcode to their function and operand type
        self.opcode_map: dict[int, tuple[Callable[[], None], Callable[[], None]]] = {
            0: (self._adv, self._get_operand_combo),
            1: (self._bxl, self._get_operand_literal),
            2: (self._bst, self._get_operand_combo),
            3: (self._jnz, self._get_operand_literal),
            4: (self._bxc, self._get_operand_literal),  # doesn't matter
            5: (self._out, self._get_operand_combo),
            6: (self._bdv, self._get_operand_combo),
            7: (self._cdv, self._get_operand_combo),
        }
        # flag that marks the end of computation
        self.stopped: bool = False
        # helper flag to stop after last fetch
        self._stop_next: bool = False

    def produce_out(self) -> str:
        """Returns the string obtained by joining the result of out instructions."""
        return ','.join(str(s) for s in self.out)

    def _disasm_operand(self, operand, op_type) -> str:
        # literal
        if op_type == self._get_operand_literal:
            return str(operand)
        # combo, the value depends on the code
        if 0 <= operand <= 3:
            return str(operand)
        elif operand == 4:
            return 'reg_a'
        elif operand == 5:
            return 'reg_b'
        elif operand == 6:
            return 'reg_c'
        # ignore incorrect 7
        return ''

    def produce_asm(self) -> str:
        """Helper function that decodes the program into readable instructions and args."""
        i = 0       # pointer to program
        instr_number = 0    # numbering
        out: str = ''
        while i < len(self.program):
            instr = self.program[i]
            operand = self.program[i+1]
            fun, op_type = self.opcode_map[instr]
            disasm_fun = fun.__name__.replace('_', '')
            disasm_op = self._disasm_operand(operand, op_type)
            # format is line_number: operation, operand
            out += f'{instr_number}:\t{disasm_fun}, {disasm_op}\n'
            # update pointer and instruction num
            instr_number += 1
            i += 2
        return out

    def fetch(self) -> None:
        """Loads the next instruction and increments instruction pointer."""
        if self.stopped:
            return
        self.curr_opcode = self.program[self.ip]
        self.curr_operand = self.program[self.ip+1]
        # for jump instructions this is incorrect but will be fixed by them
        self.ip += 2
        # if i go out of the program, stop the program
        # but don't check here, since jump can change ip

    def execute(self) -> None:
        """Executes the instructions that was just fetched."""
        # don't do anything if stopped
        if self.stopped:
            return
        # first, get the functions to do the instruction and compute operands
        fun, operand = self.opcode_map[self.curr_opcode]
        # prepare the operand in self.current_operand
        operand()
        # run the instruction
        fun()
        # this was last instruction, stop now
        # i check now because of jumps
        if self.ip >= len(self.program):
            self.stopped = True

    # all the possible instructions
    def _adv(self) -> None:
        num = self.reg_a
        den = 2 ** self.operand_value
        self.reg_a = floor(num/den)

    def _bdv(self) -> None:
        num = self.reg_a
        den = 2 ** self.operand_value
        self.reg_b = floor(num/den)

    def _cdv(self) -> None:
        num = self.reg_a
        den = 2 ** self.operand_value
        self.reg_c = floor(num/den)

    def _bxl(self) -> None:
        self.reg_b = self.reg_b ^ self.operand_value

    def _bst(self) -> None:
        self.reg_b = self.operand_value % 8

    def _jnz(self) -> None:
        if self.reg_a != 0:
            self.ip = self.operand_value

    def _bxc(self) -> None:
        self.reg_b = self.reg_b ^ self.reg_c

    def _out(self) -> None:
        self.out.append(self.operand_value % 8)

    # get the correct operand value based on the type
    def _get_operand_literal(self) -> None:
        # literal is already the correct value
        self.operand_value = self.curr_operand

    def _get_operand_combo(self) -> None:
        # the value depends on the code
        if 0 <= self.curr_operand <= 3:
            self.operand_value = self.curr_operand
        elif self.curr_operand == 4:
            self.operand_value = self.reg_a
        elif self.curr_operand == 5:
            self.operand_value = self.reg_b
        elif self.curr_operand == 6:
            self.operand_value = self.reg_c
        elif self.curr_operand == 7:
            raise RuntimeError('operand 7 is reserved and cannot be used.')

###############
# part 1
###############


# init the machine
computer = ThreeBitComputer(reg_a, reg_b, reg_c, program)

# track time
begin: float = time()
# start the program and print the output
while not computer.stopped:
    computer.fetch()
    computer.execute()
print(f'[part 1] time: {(time()-begin):.4f}s')
print(f'part 1: {computer.produce_out()}')

###############
# part 2
###############

# init the machine again (easier that writing a reset)
computer = ThreeBitComputer(reg_a, reg_b, reg_c, program)

# i need to find an input value to register A in order to have
# the output of the program matching the program itself, let's look at it
print(computer.produce_asm())

# track time
begin: float = time()

print(f'[part 2] time: {(time()-begin):.4f}s')
print(f'part 2: {0}')
