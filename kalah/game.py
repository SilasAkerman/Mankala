# Rules: https://bargames101.com/how-to-play-mancala-rules/#:~:text=%20How%20to%20Play%20Mancala:%20Rules%20for%20Popular,long%20and%20complicated%20history%20that%20spans...%20More

"""
The board consists of six rows, two columns with the board split between players in the middle
Each player also has a "store" on their side

Objective of the game is to have the most pieces in one's store
Play goes by selecting one pit and moving all pieces in it
Moving counter-clockwise (or not), one piece is dropped in each passing pit
If crossing ones store, deposit one piece here as well
Skip the opponent's store
This continues until no more pieces are left

Some extra rules:
If the last piece dropped is into one own's bowl, that player gets an extra turn
If the last piece is dropped in your half into an empty bowl and the opposite bowl is empty:
* Capture this last piece and all pieces on the opposite side into one's own store

The game ends when all pits on one player's side are empty
When this happens, the opposite player "captures" all the pieces on their half
The player with the most pieces stored wins

Variations:
The last player's opponent does not capture the rest of the pieces when the game ends
Capturing the last piece in an empty bowl is allowed even if there are no pieces in the opposite bowl
"""

import pygame
from .board import Board

class Game:
     def __init__(self, win):
          self.win = win

          self.game_init()
     
     def game_init(self):
          self.board = Board()
          self.active_player = "right"
          self.waiting_player = "left"
          self.selected = None

     def update(self):
          # self.board.draw_terminal()
          self.board.draw(self.win, self.active_player, self.selected)
          pygame.display.update()
     
     def select(self, row, col):
          # Click twice to confirm
          if row == -1:
               self.selected = None
          else:
               if self.selected == (row, col):
                    self.move(row, col)
               else:
                    self.selected = (row, col)

     def move(self, row, col, delay=None):
          if self.board.board[row][col] <= 0:
               return # Can't move if there are no pieces in the bowl
          perfect_turn = self.board.move(row, col, self.active_player, self.win, self.selected, delay)
          self.selected = None
          if not perfect_turn:
               self.alternate_turns()

     def alternate_turns(self):
          # Swap
          self.active_player, self.waiting_player = self.waiting_player, self.active_player
          self.selected = None
     
     def is_game_over(self):
          # Returns true if the game is over
          return self.board.is_game_over()

     def game_end(self):
          # All that needs to be done when the game ends
          self.update()
          pygame.time.delay(2000)
          self.board.game_end()
          self.update()

     def winner(self):
          # Returns the victor given the current board
          return self.board.winner()
     

     def ai_illustrate_move(self, move, board, delay):
          actual_board = self.board
          self.board = board
          self.move(move[0], move[1], delay)
          self.update()
          self.board = actual_board