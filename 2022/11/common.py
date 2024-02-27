from __future__ import annotations
from typing import List
import io
import re


class Item:
    def __init__(self, worry_level: int) -> None:
        self.worry_level: int = worry_level

    def __str__(self) -> str:
        return str(self.worry_level)

    def __repr__(self) -> str:
        return self.__str__()


class Arg:
    @property
    def value(self) -> int:
        ...


class OldArg(Arg):
    def __init__(self, monkey: Monkey) -> None:
        self.monkey: Monkey = monkey

    @property
    def value(self) -> int:
        return self.monkey.curr_item.worry_level


class ConstArg(Arg):
    def __init__(self, value: int) -> None:
        self._value: int = value

    @property
    def value(self) -> int:
        return self._value


class Operation:
    def do_operation(self) -> int:
        ...


class AddOperation(Operation):
    def __init__(self, arg1: Arg, arg2: Arg) -> None:
        self.arg1: Arg = arg1
        self.arg2: Arg = arg2

    def do_operation(self) -> int:
        return self.arg1.value + self.arg2.value


class MulOperation(Operation):
    def __init__(self, arg1: Arg, arg2: Arg) -> None:
        self.arg1: Arg = arg1
        self.arg2: Arg = arg2

    def do_operation(self) -> int:
        return self.arg1.value * self.arg2.value


class Monkey:
    def __init__(self, id) -> None:
        self.id: int = id
        self.items: List[Item] = []
        self.inspections_count = 0
        self.test_value: int
        self.next_if_true: int
        self.next_if_false: int
        self.curr_item: Item
        self.operation: Operation

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def inspect(self) -> None:
        self.inspections_count += 1
        self.curr_item.worry_level = self.operation.do_operation()

    def bored(self) -> None:
        self.curr_item.worry_level = self.curr_item.worry_level // 3

    def test(self) -> bool:
        return (self.curr_item.worry_level % self.test_value) == 0


def parse_operation(op: str, monkey) -> Operation:
    arg1, operator, arg2 = op.split(' ')
    if arg1 == 'old':
        arg1 = OldArg(monkey)
    else:
        arg1 = ConstArg(int(arg1))
    if arg2 == 'old':
        arg2 = OldArg(monkey)
    else:
        arg2 = ConstArg(int(arg2))
    if operator == '+':
        return AddOperation(arg1, arg2)
    return MulOperation(arg1, arg2)


def parse_monkey_params(data: io.TextIOWrapper, monkey: Monkey) -> None:
    items = re.findall(r'\d+', data.readline())
    for worry_level in items:
        monkey.add_item(Item(int(worry_level)))
    operation = data.readline().strip()[len('Operation: new = '):]
    monkey.operation = parse_operation(operation, monkey)
    monkey.test_value = int(re.findall(r'\d+', data.readline())[0])
    monkey.next_if_true = int(re.findall(r'\d+', data.readline())[0])
    monkey.next_if_false = int(re.findall(r'\d+', data.readline())[0])
