from enum import Enum
import random
import csv


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
    REMAINS_IN_RINGS = 3


class GameOutcome(Enum):
    TWO_PLAYER_TIEBREAK = 1
    THREE_PLAYER_TIEBREAK = 2
    FOUR_PLAYER_TIEBREAK = 3
    PLAYER_WINS_BY_ALL_OTHERS_ELIMINATED = 4
    PLAYER_WINS_BY_REACHING_MIDDLE = 5
    PLAYER_WINS_BY_BEING_CLOSEST_TO_MIDDLE = 6


class Player:
    won: bool
    lost: bool
    ring: int
    first: bool
    outcome: PlayerOutcome

    def __init__(self):
        self.won = False # implies they reached the middle
        self.lost = False # implies they got to the last row and failed
        self.ring = 1
        self.first = True # represents their first time being on ring 1
        self.outcome = None

    def play_turn(self, results: list[int]):
        if self.ring == 0:
            self.ring_0()

        relevant_result = results[self.ring-1]

        if self.ring == 1:
            self.ring_1(relevant_result)
        elif self.ring == 2:
            self.ring_2(relevant_result)
        else:
            self.ring_3(relevant_result)

    def ring_0(self):
        succeeded = random.randint(1, 3) in [1, 2]

        if succeeded:
            self.ring = 1
        else:
            self.lost = True
            self.outcome = PlayerOutcome.FAILS_OUTER_RING

    def ring_1(self, result: int):
        guess = random.randint(1, 2)

        if guess == result:
            self.first = False
            self.ring = 2
        elif not self.first:
            self.ring = 0

    def ring_2(self, result: int):
        guess = random.randint(1, 3)

        if guess == result:
            self.ring = 3
        else:
            self.ring = 1

    def ring_3(self, result: int):
        guess = random.randint(1, 4)

        if guess == result:
            self.won = True
            self.outcome = PlayerOutcome.REACHES_MIDDLE
        else:
            self.ring = 2


class Game:
    players: list[Player]
    turn: int
    outcome: GameOutcome

    def __init__(self):
        self.players = [Player(), Player(), Player(), Player()]
        self.turn = 0
        self.outcome = None

    def spin(self) -> list[int]:
        spin = random.randint(0, 11)
        results = [SPINNER[i][spin] for i in range(3)]

        return results

    def play(self):
        while self.turn < 10:
            self.turn += 1
            outcome = self.spin()

            for player in self.players:
                if not player.lost:
                    player.play_turn(outcome)

            self.determine_outcome()

            if self.outcome is not None:
                break
        else:
            self.determine_closeness_outcome()

        self.set_remaining_player_states()

    def determine_outcome(self):
        winning_players = 0
        losing_players = 0

        for player in self.players:
            if player.won:
                winning_players += 1
            if player.lost:
                losing_players += 1

        if winning_players == 1:
            self.outcome = GameOutcome.PLAYER_WINS_BY_REACHING_MIDDLE
        elif winning_players == 2:
            self.outcome = GameOutcome.TWO_PLAYER_TIEBREAK
        elif winning_players == 3:
            self.outcome = GameOutcome.THREE_PLAYER_TIEBREAK
        elif winning_players == 4:
            self.outcome = GameOutcome.FOUR_PLAYER_TIEBREAK

        if losing_players == 3:
            self.outcome = GameOutcome.PLAYER_WINS_BY_ALL_OTHERS_ELIMINATED
        elif losing_players == 4:
            self.outcome = GameOutcome.FOUR_PLAYER_TIEBREAK

    def determine_closeness_outcome(self):
        counts = [0, 0, 0, 0]

        for player in self.players:
            if not player.lost:
                if player.ring == 3:
                    counts[3] += 1
                elif player.ring == 2:
                    counts[2] += 1
                elif player.ring == 1:
                    counts[1] += 1
                else:
                    counts[0] += 1

        counts.reverse() # doing this for better readability in above loop

        for count in counts:
            self.determine_closeness_tie_count(count)

            if self.outcome is not None:
                break

    def determine_closeness_tie_count(self, count: int):
        if count == 0:
            return
        if count == 1:
            self.outcome = GameOutcome.PLAYER_WINS_BY_BEING_CLOSEST_TO_MIDDLE
        elif count == 2:
            self.outcome = GameOutcome.TWO_PLAYER_TIEBREAK
        elif count == 3:
            self.outcome = GameOutcome.THREE_PLAYER_TIEBREAK
        else:
            self.outcome = GameOutcome.FOUR_PLAYER_TIEBREAK

    def set_remaining_player_states(self):
        for player in self.players:
            if player.outcome is None:
                player.outcome = PlayerOutcome.REMAINS_IN_RINGS


def run(iterations: int):
    data = []

    for _ in range(iterations):
        game = Game()
        game.play()

        datum = [game.outcome.name, game.turn]

        for player in game.players:
            datum.append(player.outcome.name)

        data.append(datum)

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)

        for datum in data:
            writer.writerow(datum)
