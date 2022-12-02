from enum import Enum

data = open('./input')

points = {
    'X': 0,     # lose
    'Y': 3,     # draw
    'Z': 6      # win
}

class Plays(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __add__(self, integer):
        return self.value + integer

game_rules = {
    'A': {      # rock
        'X': Plays.SCISSORS,     # need to lose
        'Y': Plays.ROCK,         # need to draw
        'Z': Plays.PAPER         # need to win
    },
    'B': {      # paper
        'X': Plays.ROCK,         # need to lose
        'Y': Plays.PAPER,        # need to draw
        'Z': Plays.SCISSORS      # need to win
    },
    'C': {      # scissors
        'X': Plays.PAPER,        # need to lose
        'Y': Plays.SCISSORS,     # need to draw
        'Z': Plays.ROCK          # need to win
    }
}

score_per_round = []

for line in data:
    adversary, outcome = line.strip().split(' ')
    my_play = game_rules[adversary][outcome]
    score_per_round.append(my_play + points[outcome])


print(f'total score = {sum(score_per_round)}')

data.close()