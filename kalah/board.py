import pygame
from .constants import ROWS, COLS, STARTING_PIECES
from .constants import BOWL_SIZE, BOWL_PADDING_X, BOWL_PADDING_Y
from .constants import TABLE_PADDING_HEIGHT, TABLE_PADDING_WIDTH
from .constants import PIECE_SPREAD_PADDING
from .constants import WIDTH, HEIGHT, DRAW_MOVE_DELAY, CAPTURE_EMPTY, END_CAPTURE
from .drawer import Drawer
from .piece import Piece
import random

class Board:
     def __init__(self):
          self.board = []
          self.drawer = Drawer()
          self.create_board()

     def create_board(self):
          self.board.append([STARTING_PIECES for _ in range(COLS)]) # Let's presume that ROWS = 2
          self.board.append([STARTING_PIECES for _ in range(COLS)])
          self.left_store = 0
          self.right_store = 0
          self.init_pieces()
     
     def init_pieces(self):
          self.pieces = {}
          # All the pieces are stored in a dictionary with the board positions as indexes
          for row in range(ROWS):
               for col in range(COLS):
                    for _ in range(STARTING_PIECES):
                         if not (row, col) in self.pieces.keys():
                              self.pieces[(row, col)] = []
                         self.pieces[(row, col)].append(Piece(self.get_random_piece_bowl_cords(row, col)))
          # Now the stores
          self.pieces["left"] = []
          self.pieces["right"] = []
          for _ in range(self.left_store):
               self.pieces["left"].append(Piece(self.get_random_piece_store_coords("left")))
          for _ in range(self.right_store):
               self.pieces["right"].append(Piece(self.get_random_piece_store_coords("right")))
           
     
     def get_random_piece_bowl_cords(self, row, col):
          if row == 0:
               bowl_coords = (
               TABLE_PADDING_WIDTH + BOWL_PADDING_X*2 + BOWL_SIZE + BOWL_SIZE//2, 
               TABLE_PADDING_HEIGHT + BOWL_PADDING_Y + BOWL_SIZE//2
               )
          else:
               bowl_coords = (
               TABLE_PADDING_WIDTH + BOWL_PADDING_X*2 + BOWL_SIZE + BOWL_SIZE//2, 
               HEIGHT - (TABLE_PADDING_HEIGHT + BOWL_PADDING_Y + BOWL_SIZE//2)
               )
          
          bowl_coords = (bowl_coords[0] + (BOWL_SIZE + BOWL_PADDING_X)*col, bowl_coords[1])

          # Now randomize
          piece_coords = self.randomize_coords(bowl_coords, BOWL_SIZE, BOWL_SIZE)

          return piece_coords

     def get_random_piece_store_coords(self, side):
          coords = (
               TABLE_PADDING_WIDTH + BOWL_PADDING_X if side=="left" else WIDTH - (TABLE_PADDING_WIDTH + BOWL_PADDING_X + BOWL_SIZE),
               TABLE_PADDING_HEIGHT + BOWL_PADDING_Y + BOWL_SIZE//2
          )
          store_width = BOWL_SIZE*2
          store_height = (HEIGHT - (TABLE_PADDING_HEIGHT + BOWL_PADDING_Y + BOWL_SIZE//2)) - (TABLE_PADDING_HEIGHT + BOWL_PADDING_Y + BOWL_SIZE//2)
          coords = self.randomize_coords((coords[0] - BOWL_SIZE//2, coords[1]), store_width - BOWL_SIZE//2, store_height, bowl=False) # The width shouldn't need to be altered, but I don't know why)
          return coords

     def randomize_coords(self, cords, spread_x, spread_y, bowl=True):
          spread_x -= PIECE_SPREAD_PADDING
          spread_y -= PIECE_SPREAD_PADDING
          if bowl:
               cords = self.drawer.get_coords_from_center(cords[0], cords[1], BOWL_SIZE, BOWL_SIZE)
          cords = (cords[0] + PIECE_SPREAD_PADDING + random.randint(0, spread_x), cords[1] + PIECE_SPREAD_PADDING + random.randint(0, spread_y))
          return cords
     
     def draw_terminal(self):
          self.drawer.draw_terminal(self.board, self.left_store, self.right_store)
     
     def draw(self, win, active_player, selected):
          self.drawer.draw(win, self.board, self.pieces, self.left_store, self.right_store, active_player, selected)
     
     def move(self, row, col, side, draw=False, selected=None, delay=DRAW_MOVE_DELAY):
          delay = DRAW_MOVE_DELAY if delay == None else delay
          # This should also return true if the last piece went into the store
          move_list = self.get_move_list(row, col, side)
          self.board[row][col] = 0 # Empty the bowl
          self.pieces[(row, col)] = []
          for move in move_list:
               if move == "left":
                    self.left_store += 1
                    self.pieces[move].append(Piece(self.get_random_piece_store_coords(side)))
               elif move == "right":
                    self.right_store += 1
                    self.pieces[move].append(Piece(self.get_random_piece_store_coords(side)))
               else:
                    self.board[move[0]][move[1]] += 1
                    self.pieces[move].append(Piece(self.get_random_piece_bowl_cords(move[0], move[1])))
               
               if draw:
                    self.draw(draw, side, selected)
                    pygame.display.update()
                    pygame.time.delay(delay)
               
          if len(move_list[-1]) > 2: # The last move went into a store
               return True
          else:
               if self.board[move_list[-1][0]][move_list[-1][1]] <= 1:
                    self.capture(move_list[-1][0], move_list[-1][1], side)
               return False
     
     def get_move_list(self, row, col, side):
          move_list = []
          amount = self.board[row][col]
          for piece in range(amount):
               next_bowl = self.get_next_bowl(row, col, side)
               move_list.append(next_bowl)
               if len(next_bowl) > 2: # This must be a store rather than a bowl coordinate
                    row, col = next_bowl, next_bowl # Both coordinates will have the side name
               else:
                    row, col = next_bowl # Normal incrementation
          return move_list
     
     def get_next_bowl(self, row, col, side):
          # Need to fix so that this skips the opponent's store

          if row == "left":
               return 1, 0
          elif row == "right":
               return 0, COLS-1
          else:
               if row == 0:
                    col -= 1
                    if col < 0:
                         if side == "left":
                              return "left"
                         else:
                              return 1, 0
               else:
                    col += 1
                    if col >= COLS:
                         if side == "right":
                              return "right"
                         else:
                              return 0, COLS-1

          return row, col

     def capture(self, row, col, side):
          opposite_row = 0 if row == 1 else 1
          if CAPTURE_EMPTY or self.board[opposite_row][col] > 0:
               amount = 0
               amount += self.board[row][col]
               amount += self.board[opposite_row][col]
               if side == "left":
                    self.left_store += amount
               else:
                    self.right_store += amount
               
               for _ in range(amount):
                    self.pieces[side].append(Piece(self.get_random_piece_store_coords(side)))

               self.board[row][col] = 0
               self.board[opposite_row][col] = 0
               self.pieces[(row, col)] = []
               self.pieces[(opposite_row, col)] = []
                    

     def is_game_over(self):
          # Is the game over?
          left_side = self.board[0][:COLS//2]
          left_side.extend([self.board[1][i] for i in range(COLS//2)])
          right_side = self.board[0][COLS//2:]
          right_side.extend([self.board[1][i] for i in range(COLS//2, COLS)])

          if sum(left_side) <= 0:
               return "left"
          if sum(right_side) <= 0:
               return "right"

          return False
     
     def game_end(self):
          # All that needs to be done when the game ends
          side_end =  "left" if self.is_game_over() == "right" else "right"
          if END_CAPTURE:
               # Since one half is already empty, gathering all the pieces alright
               amount = 0
               for row in range(ROWS):
                    for col in range(COLS):
                         amount += self.board[row][col]
                         self.board[row][col] = 0
                         self.pieces[(row, col)] = []

               if side_end == "left":
                    self.left_store += amount
               if side_end == "right":
                    self.right_store += amount

               for _ in range(amount):
                    self.pieces[side_end].append(Piece(self.get_random_piece_store_coords(side_end)))
     
     def winner(self):
          # Assume the game is over and all the procedure is done
          return "left" if self.left_store > self.right_store else "right" if self.right_store > self.left_store else "draw"
     

     def get_available_bowls(self):
          available_coords = []
          for row in range(ROWS):
               for col in range(COLS):
                    if self.board[row][col] > 0:
                         available_coords.append((row, col))
          return available_coords
     
     def ai_evaluate(self, ai_side):
          # Let's at first just return the difference in the score from the ai's perspective
          if ai_side == "left":
               return self.left_store - self.right_store
          else:
               return self.right_store - self.left_store