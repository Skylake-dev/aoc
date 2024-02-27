from typing import Generator, List, Tuple


class Tree:
    def __init__(self, height: int) -> None:
        self.height: int = height
        self.visible: bool = False
        self.scenic_score: int = 0

    def __str__(self) -> str:
        return str(self.height)

    def __repr__(self) -> str:
        return self.__str__()


class Forest:
    def __init__(self) -> None:
        self.trees: List[List[Tree]] = []

    def add_row(self, row: List[Tree]):
        self.trees.append(row)

    def get_tree(self, row, col) -> Tree:
        return self.trees[row][col]

    def dimensions(self) -> Tuple[int, int]:
        return len(self.trees), len(self.trees[0])

    def get_row(self, index: int) -> List[Tree]:
        return self.trees[index]

    def get_col(self, index: int) -> List[Tree]:
        column = []
        for row in self.trees:
            column.append(row[index])
        return column

    def cols_top_to_bottom(self) -> Generator[List[Tree], None, None]:
        for j in range(len(self.trees[0])):
            column: List[Tree] = []
            for i in range(len(self.trees)):
                column.append(self.trees[i][j])
            yield column

    def cols_bottom_to_top(self) -> Generator[List[Tree], None, None]:
        for col in self.cols_top_to_bottom():
            yield list(reversed(col))

    def rows_left_to_right(self) -> Generator[List[Tree], None, None]:
        for row in self.trees:
            yield row

    def rows_right_to_left(self) -> Generator[List[Tree], None, None]:
        for row in self.rows_left_to_right():
            yield list(reversed(row))

    def count_visible(self) -> int:
        visible = 0
        for row in self.trees:
            for tree in row:
                if tree.visible:
                    visible += 1
        return visible


def compute_visibility(trees: List[Tree]) -> None:
    trees[0].visible = True
    current_height = trees[0].height
    for tree in trees:
        if tree.height > current_height:
            tree.visible = True
            current_height = tree.height
