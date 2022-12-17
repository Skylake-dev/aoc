from common import (
    Valve,
    best_path,
    connect,
    parse_input
)
from typing import Dict, List

valves: Dict[str, Valve] = {}

with open('./input') as data:
    valves = parse_input(data)

connect(valves)
starting_valve = valves['AA']
# keep track only of valves that have flow
useful_valves: List[Valve] = []
for id in valves:
    if valves[id].flow_rate != 0:
        useful_valves.append(valves[id])

available_time = 30

path, total_pressure_released = best_path(
    starting_valve, useful_valves, available_time)

print(f'max presure released = {total_pressure_released}')
