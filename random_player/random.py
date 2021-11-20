import random

def get_random_move(board):
     return random.choice(board.get_available_bowls())