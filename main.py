import random
import pygame
from shapes import shapes, shapes_colors

block_size = 22
screen_width = 22
screen_height = 33
game_FPS = 10


pygame.init()
screen = pygame.display.set_mode((screen_width*block_size, screen_height*block_size))

font1 = pygame.font.Font('roboto.ttf', 65)
font2 = pygame.font.Font('roboto.ttf', 25)
tetris_text = font1.render("Tetris", True, (255, 255, 255))
press_text = font2.render("Press SPACE to play", True, (200, 200, 200))

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

def lock_check(current_piece_coordinates, grid, score):
    locked = False


    for (x, y) in current_piece_coordinates:            
        if y >= screen_height:
            locked = True
        else:
            if grid[y][x] == "lock" and y >= 0:
                locked = True

        if locked and y == 0:
            game_over(score=score)

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

def game_over(score):
    pygame.time.delay(2000//game_FPS)
    main_menu(score)


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
    current_piece = Piece(screen_width//2, -4, random.choice(shapes))
    locked_positions = []
    grid = update_grids()
    score = 0

    while True:
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
        screen.fill((30, 32, 33))
        pygame.draw.rect(screen, (120, 50, 50), (0, 0, screen_width*block_size, block_size))
        draw_grid(screen, grid, current_piece.color)

        pygame.display.update()
        
        # GAME LOGIC
        current_piece.y += 1

        if lock_check(current_piece.coordinates(), grid, score=score):
            current_piece.y -= 1
            for coordinate in current_piece.coordinates():
                locked_positions.append(coordinate)

            current_piece = Piece(screen_width//2, -4, random.choice(shapes))

        locked_positions, score = delete_rows(score, locked_positions)

        grid = update_grids(
            locked_positions=locked_positions, 
            current_piece_coordinates=current_piece.coordinates()
        )
        
def main_menu(score=None):
    show_text = True
    score_text_title = font2.render("score:", True, (200, 200, 200))
    score_text_quant = font1.render(str(score), True, (215, 215, 215))

    while True:
        # EVENTS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        screen.fill((30, 32, 33))
        screen.blit(tetris_text, (screen_width*block_size//2 - tetris_text.get_width() // 2, round(screen_height*block_size//2 - tetris_text.get_height() // 2) - 6 * block_size))
        if show_text:
            screen.blit(press_text, (screen_width*block_size//2 - press_text.get_width() // 2, round(screen_height*block_size//2 - press_text.get_height() // 2) - 2 * block_size))
        
        if score != None:
            screen.blit(score_text_title, (screen_width*block_size//2 - score_text_title.get_width() // 2, round((screen_height*block_size//2 - score_text_title.get_height() // 2)) + 1.5 * block_size))
            screen.blit(score_text_quant, (screen_width*block_size//2 - score_text_quant.get_width() // 2, round((screen_height*block_size//2 - score_text_quant.get_height() // 2)) + 3 * block_size))



        pygame.display.update()

        pygame.time.delay(500)
        show_text = not show_text


main_menu()