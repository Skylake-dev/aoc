from typing import Iterator

# accumulate result
result: int = 0
# flag for the do and don't
do: bool = True
# flag to specify whether to account for do and dont
active_do_and_dont: bool = False


def text(s: str) -> Iterator[str]:
    """Returns the next character from the input string."""
    for char in s:
        yield char


def mul(input_tape: Iterator[str]) -> None:
    """procedure to parse the muls"""
    global result, do, active_do_and_dont
    op1: str = ''
    op2: str = ''
    next_char: str = next(input_tape)
    # at this point i already consumed the initial m
    if next_char == 'u':
        next_char = next(input_tape)
        if next_char == 'l':
            next_char = next(input_tape)
            if next_char == '(':
                # need to read all digits
                next_char = next(input_tape)
                # if no digit return immediately
                if not next_char.isdigit():
                    return
                # otherwise keep reading digits and append to op1
                while next_char.isdigit():
                    op1 += next_char
                    next_char = next(input_tape)
                if next_char == ',':
                    # at this point i expect to find digits for op2
                    next_char = next(input_tape)
                    # if no digit return immediately
                    if not next_char.isdigit():
                        return
                    # otherwise, same as before keep appending digits to op2
                    while next_char.isdigit():
                        op2 += next_char
                        next_char = next(input_tape)
                    if next_char == ')':
                        # i completed a mul parsing, compute the result
                        # but only if the do flag is active
                        if do:
                            result += int(op1) * int(op2)
    # all the else clauses are simple return so i don't need anything else


def do_and_dont(input_tape: Iterator[str]) -> None:
    """procedure to parse the dos and donts"""
    global result, do, active_do_and_dont
    if not active_do_and_dont:
        # if they are not active don't do anything
        return
    next_char: str = next(input_tape)
    # similarly to mul, i already read the first character
    # so start from 'o'
    if next_char == 'o':
        next_char = next(input_tape)
        if next_char == '(':
            next_char = next(input_tape)
            if next_char == ')':
                # i read a complete do(), set active
                do = True
        elif next_char == 'n':
            # here i actually have to check whether
            # i have a do() or don't()
            next_char = next(input_tape)
            if next_char == '\'':
                next_char = next(input_tape)
                if next_char == 't':
                    next_char = next(input_tape)
                    if next_char == '(':
                        next_char = next(input_tape)
                        if next_char == ')':
                            # i read a complete don't(), set inactive
                            do = False
    # all the else clauses are simple return so i don't need anything else


def parse(input_tape: Iterator[str]) -> None:
    """entry point for the parser"""
    global result, do, active_do_and_dont
    while True:
        try:
            next_char: str = next(input_tape)
        except StopIteration:
            # when i finish input, return
            return
        else:
            if next_char == 'm':
                # check if it is a valid mul
                mul(input_tape)
            elif next_char == 'd':
                # check if it is a do or dont
                do_and_dont(input_tape)
            # ignore all other chars


def main() -> None:
    global result, do, active_do_and_dont
    with open('./input') as f:
        input = f.readlines()
    # join all lines
    s: str = ''.join(input)
    # start parsing, do and don't disabled
    input_tape = text(s)
    parse(input_tape)
    print(f'part 1 {result}')
    # rewind the tape and enable do and don't
    input_tape = text(s)
    active_do_and_dont = True
    result = 0
    parse(input_tape)
    print(f'part 2 {result}')


if __name__ == '__main__':
    main()
