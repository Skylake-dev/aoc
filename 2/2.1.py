from enum import Enum

data = open('./input')

points = {
    'X': 1,     # rock
    'Y': 2,     # paper
    'Z': 3      # scissors
}

class Outcomes(Enum):
    WIN = 6
    DRAW = 3
    LOSE = 0

    def __add__(self, integer):
        return self.value + integer

game_rules = {
    'X': {      # rock
        'A': Outcomes.DRAW,     # rock
        'B': Outcomes.LOSE,     # paper
        'C': Outcomes.WIN       # scissors
    },
    'Y': {      # paper
        'A': Outcomes.WIN,      # rock
        'B': Outcomes.DRAW,     # paper
        'C': Outcomes.LOSE      # scissors
    },
    'Z': {      # scissors
        'A': Outcomes.LOSE,     # rock
        'B': Outcomes.WIN,      # paper
        'C': Outcomes.DRAW      # scissors
    },
}

score_per_round = []

for line in data:
    adversary, choice = line.strip().split(' ')
    outcome = game_rules[choice][adversary]
    score_per_round.append(outcome + points[choice])

print(f'total score = {sum(score_per_round)}')

data.close()