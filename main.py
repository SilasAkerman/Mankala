import pygame
from kalah.game import Game
from kalah.constants import WIDTH, HEIGHT
from kalah.constants import ROWS, COLS
from kalah.constants import TABLE_PADDING_HEIGHT, TABLE_PADDING_WIDTH
from kalah.constants import BOWL_PADDING_X, BOWL_PADDING_Y, BOWL_SIZE
from random_player.random import get_random_move
from minimax.algorithm import minimax

FPS = 10

AI_TURN_1 = "left"
AI_DEPTH_1 = 4
AI_TURN_2 = "righ"
AI_DEPTH_2 = 6
AI_DELAY = 0

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kalah")

def get_row_col_from_mouse(mouse_coords):
     init_coords = (
               TABLE_PADDING_WIDTH + BOWL_PADDING_X*2 + BOWL_SIZE + BOWL_SIZE//2, 
               TABLE_PADDING_HEIGHT + BOWL_PADDING_Y + BOWL_SIZE//2
          )
     bowl_coords = []
     for row in range(ROWS):
          for col in range(COLS):
               bowl_coords.append((init_coords[0] + (BOWL_SIZE + BOWL_PADDING_X)*col, 
               (HEIGHT - init_coords[1] if row == 1 else init_coords[1])))

     row, col = 0, 0
     for bowl in bowl_coords:
          if (pow(mouse_coords[0] - bowl[0], 2) + pow(mouse_coords[1] - bowl[1], 2)) ** 0.5 < BOWL_SIZE:
               return row, col
          col += 1
          if col >= COLS:
               row += 1
               col = 0
               
     
     return -1, -1



def main():
     run = True
     game_over = False
     clock = pygame.time.Clock()
     game = Game(WIN)
     game.update()

     while run:
          clock.tick(FPS)

          # Here goes all the ai
          ai_has_moved = False

          if game.active_player == AI_TURN_1 and not game_over and not ai_has_moved:
               pygame.time.delay(AI_DELAY)
               move = minimax(game.board, AI_DEPTH_1, AI_TURN_1, game)[0]
               game.select(move[0], move[1])
               game.move(move[0], move[1])
               game.update()
               ai_has_moved = True

          
          if game.active_player == AI_TURN_2 and not game_over and not ai_has_moved:
               pygame.time.delay(AI_DELAY)
               move = minimax(game.board, AI_DEPTH_2, AI_TURN_2, game)[0]
               game.select(move[0], move[1])
               game.move(move[0], move[1])
               game.update()
               ai_has_moved = True


          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    run = False
               
               if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not (game.active_player == AI_TURN_1 or game.active_player == AI_TURN_2):
                    row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                    game.select(row, col)
               
               if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_p and game_over) or (event.key == pygame.K_r):
                         game.game_init()
                         game_over = False
                    if event.key == pygame.K_BACKSPACE:
                         run = False
          
          if game.is_game_over() and not game_over:
               game_over = True
               game.game_end()
               print(game.winner())
          
          game.update()
          
     
     pygame.quit()



if __name__ == "__main__":
     main()