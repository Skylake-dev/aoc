from __future__ import annotations
from io import TextIOWrapper
import time
from typing import Any, Dict, Generator, List, Set, Tuple

MISSING: Any = None


class Connection:
    def __init__(self, valve: Valve, hops: int) -> None:
        self.valve: Valve = valve
        self.hops: int = hops

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Connection):
            return False
        return self.valve == __o.valve


class Valve:
    def __init__(self, id: str, flow_rate: int = MISSING) -> None:
        self.id: str = id
        self.flow_rate: int = flow_rate
        self.connected: Dict[str, Connection] = {}

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return self.__str__()

    def print_conn(self) -> None:
        s = f'{self.id} connected to '
        for c in self.connected.values():
            s += f'{c.valve.id}({c.hops}) '
        print(s)


def compute_released_pressure(path: List[Valve], time: int) -> int:
    ...


# def recursive_path_builder(start: Valve, relevant_valves: Set[Valve], time_left: int) -> Generator[List[Valve], None, None]:
#     # return all feasible paths between the relevant valves (flow > 0) given the time constraint
#     path = [start]
#     if time_left < 2:  # to move and open 2 minutes are required
#         yield path
#         return
#     for conn in start.connected.values():
#         if conn.valve in relevant_valves:
#             new_time = time_left - conn.hops
#             for extension in recursive_path_builder(conn.valve, relevant_valves, new_time):
#                 yield path + extension
def recursive_path_builder(current_path: List[Valve], relevant_valves: List[Valve], time_left: int) -> Generator[List[Valve], None, None]:
    # return all feasible paths between the relevant valves (flow > 0) given the time constraint
    if time_left < 2:  # to move and open 2 minutes are required
        yield current_path
        return
    if not relevant_valves:   # no more valves to open
        yield current_path
        return
    for conn in current_path[-1].connected.values():
        v = conn.valve
        if v in relevant_valves:
            if len(current_path) > 2 and v == current_path[-2]:
                continue
            new_time = time_left - conn.hops
            # i need a better condition to avoid long paths going back and forth
            for extension in recursive_path_builder(current_path + [conn.valve], relevant_valves, new_time):
                yield extension


def best_path(starting_valve: Valve, valves: List[Valve], time: int) -> Tuple[List[Valve], int]:
    # build all possible going from one useful valve to another
    # and choose the one that releases the most pressure
    best_path = []
    max = 0
    for i, path in enumerate(recursive_path_builder([starting_valve], valves, time)):
        if i % 100000 == 0:
            print(path, i)
        score = compute_released_pressure(path, time)
        if score > max:
            max = score
            best_path = path
    return best_path, max


def _connect_recursive(valves: Dict[str, Valve]) -> bool:
    unchanged = True
    for id in valves:
        valve = valves[id]
        next_ids = [c for c in valve.connected]
        for next_id in next_ids:
            next_hop = valve.connected[next_id].valve
            next_next_ids = [c for c in next_hop.connected]
            for next_next_id in next_next_ids:
                next_next_hop = next_hop.connected[next_next_id].valve
                if next_next_id == id:
                    # skip self loop
                    continue
                if next_next_id in valve.connected:
                    # already present, check if it is shorter
                    if valve.connected[next_next_id].hops > next_hop.connected[next_next_id].hops + valve.connected[next_id].hops:
                        valve.connected[next_next_id].hops = next_hop.connected[next_next_id].hops + \
                            valve.connected[next_id].hops
                        unchanged = False
                else:
                    # not present, add new connection
                    valve.connected[next_next_id] = Connection(
                        next_next_hop, next_hop.connected[next_next_id].hops + valve.connected[next_id].hops)
                    unchanged = False
    return unchanged


def connect(valves: Dict[str, Valve]) -> None:
    unchanged = False
    i = 1
    while not unchanged:
        unchanged = _connect_recursive(valves)
        i += 1


def parse_input(data: TextIOWrapper) -> Dict[str, Valve]:
    valves: Dict[str, Valve] = {}
    for line in data:
        valve, connection = line.strip().split(';', 2)
        id: str = valve[6:8]
        flow_rate: int = int(valve[23:])
        if id in valves:
            curr_valve = valves[id]
            curr_valve.flow_rate = flow_rate
        else:
            curr_valve = Valve(id, flow_rate)
            valves[id] = curr_valve
        connected = connection.split(',')
        for value in connected:
            id = value[-2:]
            if id in valves:
                to_connect = valves[id]
            else:
                to_connect = Valve(id)
                valves[id] = to_connect
            curr_valve.connected[to_connect.id] = Connection(to_connect, 1)
    return valves
