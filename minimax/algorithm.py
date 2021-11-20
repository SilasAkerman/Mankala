from copy import deepcopy

import pygame

DRAW_MOVES = False
DRAW_MOVES_DELAY = 0
AI_SIDE = "left"

def minimax(board, depth, side, game):
     # Returns a value and a bowl move
     if depth <= 0 or board.is_game_over():
          if board.is_game_over():
               board.game_end()
          return None, board.ai_evaluate(side) # The move is determined one level up
     
     max_evaluation = float("-inf")
     best_move = None
     other_side = "left" if side == "right" else "right"

     for move in board.get_available_bowls():
          player_change = -1
          new_board = deepcopy(board)
          perfect_turn = new_board.move(move[0], move[1], side)

          if DRAW_MOVES:
               draw_move(move, new_board, game)
               pygame.time.delay(DRAW_MOVES_DELAY)

          if perfect_turn: # In this game, a perfect move is rewarded with another turn. Hence, back to maximizing
               player_change = 1
               side, other_side = other_side, side

          evaluation = player_change * minimax(new_board, depth-1, other_side, game)[1] # We want the worst move from the previous player as our maximizer. Therefore, multiply by -1 (except for perfect turn)
          max_evaluation = max(max_evaluation, evaluation)

          if max_evaluation == evaluation:
               best_move = move # Update the move

     
     return best_move, max_evaluation


def draw_move(move, board, game):
     board = deepcopy(board)
     game.selected = move
     game.ai_illustrate_move(move, board, DRAW_MOVES_DELAY)
     game.selected = None