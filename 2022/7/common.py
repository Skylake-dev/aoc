from __future__ import annotations
from typing import Any, List, Union

MISSING: Any = None


class File:
    def __init__(self, name: str, size: Union[int, str]) -> None:
        self.name: str = name
        self.size: int = int(size)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, File):
            return False
        return (self.name == other.name) and (self.size == other.size)

    def __str__(self) -> str:
        return self.name


class Directory:
    def __init__(self, name: str, parent: Directory = MISSING) -> None:
        self.name: str = name
        if parent is MISSING and name != '/':
            raise RuntimeError('only root can have missing parent')
        self.parent: Directory = parent
        self.subdirs: List[Directory] = []
        self.files: List[File] = []
        self.size: int = 0

    def __str__(self) -> str:
        return self.name

    def add_file(self, file: File) -> None:
        if any((file == f) for f in self.files):
            return
        self.files.append(file)
        self.size += file.size
        # update size of all parents
        # the alternative would be to compute size recursively each time idk which is better
        up_dir = self.parent
        while(up_dir != MISSING):
            up_dir.size += file.size
            up_dir = up_dir.parent

    def add_subdir(self, dir: Directory) -> None:
        if any((dir.name == d.name) for d in self.subdirs):
            return
        self.subdirs.append(dir)
        # only affects size if dir is not empty
        self.size += dir.size


root: Directory = Directory('/')


def process_command(command: str, cwd: Directory) -> Directory:
    if command[2:4] == 'ls':
        return cwd
    # change cwd
    arg = command[5:].strip()
    if arg == '/':
        cwd = root
    elif arg == '..':
        if cwd is root:
            raise RuntimeError('root has no parent')
        cwd = cwd.parent
    else:
        # assumes subdir alreay exists
        for dir in cwd.subdirs:
            if dir.name == arg:
                cwd = dir
                break
    return cwd


def process_output(line: str, cwd: Directory) -> None:
    args = line.strip().split(' ')
    if args[0] == 'dir':
        new_dir = Directory(args[1], cwd)
        cwd.add_subdir(new_dir)
    else:
        new_file = File(args[1], args[0])
        cwd.add_file(new_file)


def walk_tree(start_dir: Directory):
    for dir in start_dir.subdirs:
        for subdir in walk_tree(dir):
            yield subdir
    yield start_dir
