import random
import pygame
from shapes import shapes, shapes_colors

block_size = 20
screen_width = 20
screen_height = 30
game_FPS = 10


pygame.init()
screen = pygame.display.set_mode((screen_width*block_size, screen_height*block_size))
pygame.display.set_caption('Tetris') 

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapes_colors[shapes.index(shape)]
        self.rotation = 0

    def coordinates(self):
        coordinates = []
        for row in range(len(self.shape[self.rotation % len(self.shape)])):
            for col in range(len(self.shape[self.rotation % len(self.shape)][row])):
                if self.shape[self.rotation % len(self.shape)][row][col] == "0":
                    cord = (self.x+col, self.y+row)
                    coordinates.append(cord)

        return coordinates

'''
    LOGIC FUNCTIONS
'''

def update_grids(locked_positions=[], current_piece_coordinates=[]):
    grid = []
    for row in range(screen_height):
        current_row = []
        for col in range(screen_width):
            if (col, row) in locked_positions:
                current_row.append("lock")
            elif (col, row) in current_piece_coordinates:
                current_row.append("current")
            else:
                current_row.append(".")
        grid.append(current_row)
    
    return grid

def valid_move(current_piece_coordinates, grid):
    valid = True

    for (x, y) in current_piece_coordinates:
        if x > screen_width or x < 0:
            valid = False
        else:
            try:
                if grid[y][x] == "lock":
                    valid = False
            except IndexError:
                valid = False

    return valid

def lock_check(current_piece_coordinates, grid):
    locked = False


    for (x, y) in current_piece_coordinates:            
        if y >= screen_height:
            locked = True
        else:
            if grid[y][x] == "lock" and y >= 0:
                locked = True

        if locked and y == 0:
            game_over()

    return locked


def delete_rows(score, locked_positions=[]):
    for row in range(screen_height):
        index_to_remove = []
        for (x, y) in locked_positions:
            if y == row:
                index_to_remove.append(locked_positions.index((x,y)))

        if len(index_to_remove) == screen_width:
            index_to_remove.reverse()
            for index in index_to_remove:
                locked_positions.pop(index)
                score += 1
            for (x, y) in locked_positions:
                index = locked_positions.index((x,y))
                if y < row:
                    coordinate = (x, y+1)
                    locked_positions[index] = coordinate


            delete_rows(locked_positions)

    return locked_positions, score

def game_over():
    pygame.time.delay(2000//game_FPS)
    main()


'''
    VIEW FUNCTIONS
'''
 
def draw_grid(surface, grid, current_piece_color):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            color = (120,120,120)
            if grid[row][col] == "current":
                color = current_piece_color
            elif grid[row][col] == ".":
                continue
            pygame.draw.rect(surface, color, (col*block_size, row*block_size, block_size, block_size))


def main():
    run = True
    current_piece = Piece(screen_width//2, -4, random.choice(shapes))
    locked_positions = []
    grid = update_grids()
    score = 0

    while run:
        # EVENTS
        
        pygame.time.delay(1000//game_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_move(current_piece.coordinates(), grid)):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_move(current_piece.coordinates(), grid)):
                        current_piece.x -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_move(current_piece.coordinates(), grid)):
                        current_piece.rotation -= 1
                
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_move(current_piece.coordinates(), grid)):
                        current_piece.y -= 1
                elif event.key == pygame.K_r:
                    main()

        # GAME SCREEN
        pygame.draw.rect(screen, (30, 32, 33), (0,0,screen_width*block_size, screen_height*block_size))
        pygame.draw.rect(screen, (255, 50, 50, 12), (0, 0, screen_width*block_size, block_size))
        draw_grid(screen, grid, current_piece.color)

        pygame.display.update()
        
        # GAME LOGIC
        current_piece.y += 1

        if lock_check(current_piece.coordinates(), grid):
            current_piece.y -= 1
            for coordinate in current_piece.coordinates():
                locked_positions.append(coordinate)

            current_piece = Piece(screen_width//2, -4, random.choice(shapes))

        locked_positions, score = delete_rows(score, locked_positions)

        grid = update_grids(
            locked_positions=locked_positions, 
            current_piece_coordinates=current_piece.coordinates()
        )
        
def main_menu(score):
    return


main()