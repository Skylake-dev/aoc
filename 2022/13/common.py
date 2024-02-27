from typing import List, Optional, Union


def iteratio_and_run_out(left_len, right_len):
    if left_len > right_len:
        iterate_until = right_len
        run_out_value = False
    elif left_len < right_len:
        iterate_until = left_len
        run_out_value = True
    else:
        iterate_until = right_len
        run_out_value = None
    return iterate_until, run_out_value


def _compare_int(left: int, right: int) -> Optional[bool]:
    if left < right:
        return True
    elif left > right:
        return False
    else:
        return None


def _compare_lists(left: list, right: list) -> Optional[bool]:
    left_len = len(left)
    right_len = len(right)
    iterate_until, run_out_value = iteratio_and_run_out(left_len, right_len)
    for i in range(iterate_until):
        curr_left = left[i]
        curr_right = right[i]
        result = _right_order(curr_left, curr_right)
        if result is not None:
            return result
    return run_out_value


def _right_order(curr_left, curr_right) -> Optional[bool]:
    if isinstance(curr_left, int):
        if isinstance(curr_right, int):
            result = _compare_int(curr_left, curr_right)
            if result is not None:
                return result
        if isinstance(curr_right, list):
            curr_left = [curr_left]
            result = _compare_lists(curr_left, curr_right)
            if result is not None:
                return result
    elif isinstance(curr_left, list):
        if isinstance(curr_right, int):
            curr_right = [curr_right]
            result = _compare_lists(curr_left, curr_right)
            if result is not None:
                return result
        if isinstance(curr_right, list):
            result = _compare_lists(curr_left, curr_right)
            if result is not None:
                return result


def right_order(left: list, right: list) -> Optional[bool]:
    left_idx = 0
    right_idx = 0
    iterate_until, run_out_value = iteratio_and_run_out(len(left), len(right))
    for i in range(iterate_until):
        curr_left = left[left_idx]
        curr_right = right[right_idx]
        result = _right_order(curr_left, curr_right)
        if result is not None:
            return result
        left_idx += 1
        right_idx += 1
    return run_out_value
