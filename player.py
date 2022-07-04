import math
import random


class Player:
    def __init__(self,letter):
        # Get's player's letter whether 'x' or 'o'
        self.letter = letter

    def get_move(self, game):
        pass


class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square # return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ")
            # check whether it is a number and it is in available moves
            # if not raise an error and repeat
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True # if in available move
            except ValueError:
                print('Invalid square, Try again!')

        return val


# Genius computer never loses. It has been trained. only wins and ties
class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly chose a square
        else:
            # get square using minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # yourself
        other_player = 'O' if player == 'X' else 'X'

        # BASE CASE: check if previous move is a winner
        if state.current_winner == other_player:
            # keep track: return position and score
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
                    }

        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0}

        
        # REAL CASE. The real minimax algorithm in 4 steps
        #  before, initialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # STEP 1: make a move, try that spot
            state.make_move(possible_move, player)

            # STEP 2: recurse using minimax to simulate game after making that move
            sim_score = self.minimax(state, other_player) # we alternate to the other player to check his score

            # STEP 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # STEP 4: update dictionaries if necessary
            if player == max_player: # maximize the player
                if sim_score['score'] > best['score']:
                    best = sim_score # replace the best
            else: # minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score # replace the best

        return best
