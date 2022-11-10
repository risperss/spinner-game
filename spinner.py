from enum import Enum
import random

turns = 0
winner = False
first_attempt = True



def stage_1():
    while True:
        guess = random.randint(1, 2)
        turns += 1
        if guess == 1:
            first_attempt = False
            stage_2()
        elif not first_attempt:
            stage_0()

def stage_2():
    while True:
        guess = random.randint(1, 3)
        turns += 1
        if guess == 1:
            stage_3()
        else:
            stage_1()

def stage_3():
    while True:
        guess = random.randint(1, 4)
        turns += 1
        if guess == 1:
            winner = True
        else:
            stage_2()

def stage_0():
    guess = random.randint(1, 3)

    if guess in [1, 2]:
        stage_1()


# 1. you get to the middle
# 2. you go outside and lose
# 3. you run out of turns
# 4. probability of running out of turns on a given ring
# 5. tbd


# 3 rows divided into 4ths or 3rds, therefore 12 parts
# We can ignore ring 0 because the player is not making a guess
SPINNER = [
    [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
]


class PlayerOutcome(Enum):
    REACHES_MIDDLE = 1
    FAILS_OUTER_RING = 2
    RUNS_OUT_OF_TURNS = 3


class GameOutcome(Enum):
    TWO_PLAYER_TIEBREAK = 1
    THREE_PLAYER_TIEBREAK = 2
    FOUR_PLAYER_TIEBREAK = 3
    PLAYER_WINS_BY_ELIMINATION = 4
    PLAYER_WINS_BY_REACHING_MIDDLE = 5
    PLAYER_WINS_BY_BEING_CLOSEST_TO_MIDDLE = 6


class Player:
    id: int
    won: bool
    ring: int
    first: bool

    def __init__(self, id: int):
        self.id = id
        self.won = False # implies they reached the middle
        self.ring = 1
        self.first = True # represents their first time being on the outer ring

    def play_turn(self, outcome: list[int]):
        ...

    def ring_0(self):
        return random.randint(1, 3) in [1, 2]

    def ring_1(self, outcome: int):
        guess = random.randint(1, 2)

        if guess == outcome:
            self.ring = 2
        elif not self.first:
            self.ring = 0

    def ring_2(self, outcome: int):
        guess = random.randint(1, 3)

        if guess == outcome:
            self.ring = 3
        else:
            self.ring = 2

    def ring_3(self, outcome: int):
        guess = random.randint(1, 4)


class Game:
    players: list[Player]
    turn: int

    def __init__(self):
        self.players = [Player(1), Player(2), Player(3), Player(4)]
        self.turn = 0

    def spin(self) -> list[int]:
        spin = random.randint(0, 11)
        outcome = [SPINNER[i][spin] for i in range(3)]

        return outcome
