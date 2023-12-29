# Tic Tac Toe
# extends the code TTT-grid.py posted in Week 9 of eclass to create a 2 player game
# has end of game condition
# Author - Dhruvraj Singh
import pygame,random

# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Tic Tac Toe')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        # create board as an empty list
        self.flashers = [] # holds the tiles that will flash at the end of the game
        self.filled_count = 0
        self.board_size = 3
        self.board = []
        self.create_board()
        self.player_x = 'X'
        self.player_o = 'O'
        self.turn = self.player_x

    def create_board(self):
        # creates the board
        # -self is the Game object
        width = self.surface.get_width()//3
        height = self.surface.get_height()//3
        # for each row index
        for row_index in range(0,self.board_size):
            # create row as an empty list
            row = []
            # for each column index
            for col_index in range(0,self.board_size):
                # create tile using row index and column index
                x = col_index * width 
                y = row_index * height
                tile = Tile(x,y,width,height,self.surface)
                # append tile to row
                row.append(tile)
            # append row to board
            self.board.append(row)      

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos)

    def handle_mouse_up(self,position):
        # handle mouse up event
        # - self is the Game object
        # - position is the (x,y) location of the mouse click of type tuple
        for row in self.board:
            for tile in row:
                if tile.select(position,self.turn):
                    self.filled_count = self.filled_count + 1
                    self.change_turn()

    def change_turn(self):
        # changes the turn in the Game
        # - self is the Game object

        if self.turn == self.player_x:
            self.turn = self.player_o
        else:
            self.turn = self.player_x

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        if not self.continue_game: # when the game has stopped
            tile = random.choice(self.flashers)
            # tile.flashing = True # violating SW quality
            tile.set_flashing_on() #sets self.flashing to True
        # draw the board
        for row in self.board:
            for tile in row:
                tile.draw()
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        pass
    
    def is_row_win(self):
        win = False
        list_of_lists_of_tiles = self.board
        if self.contains_list_win(list_of_lists_of_tiles):
            win = True
        return win

    def contains_list_win(self,list_of_lists_of_tiles):
        # checks if there is a list win
        win = False
        for list_of_tiles in list_of_lists_of_tiles:
            if self.is_list_win(list_of_tiles):
                win = True
        return win

    def is_list_win(self,list_of_tiles):
        # checks if a list has tiles with the same content
        same = True
        first = list_of_tiles[0]
        for tile in list_of_tiles:
            if not (tile.equal(first)):
                same = False
        if same:
            self.flashers.extend(list_of_tiles)
            #for tile in list_of_tiles:
            #   self.flashers.append(tile)
        return same

    def is_column_win(self):
        # check for column win
        win = False
        list_of_lists_of_tiles =[]
        for col_index in range(0,self.board_size):
            column = []
            for row in self.board:
                column.append(row[col_index])
            list_of_lists_of_tiles.append(column)
        if self.contains_list_win(list_of_lists_of_tiles):
            win = True
        return win
    
    def is_diagonal_win(self):
        # check for a diagonal win
        win = False
        list_of_lists_of_tiles = []
        diagonal1 = []
        diagonal2 = []
        for index in range(0,self.board_size):
            diagonal1.append(self.board[index][index])
            diagonal2.append(self.board[index][self.board_size - index -1])
        
        list_of_lists_of_tiles.append(diagonal1)
        list_of_lists_of_tiles.append(diagonal2)
        
        if self.contains_list_win(list_of_lists_of_tiles):
            win = True
        
        return win

    def is_win(self):
        win = False
        row_win = self.is_row_win()
        column_win = self.is_column_win()
        diagonal_win = self.is_diagonal_win()
        if row_win or column_win or diagonal_win:
            win = True
        return win
    
    def is_tie(self):
        tie = False
        if self.filled_count == self.board_size**2:
            tie = True
        if tie:
            for row in self.board:
                for tile in row:
                    self.flashers.append(tile)
        return tie

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        if self.is_win() or self.is_tie():
            self.continue_game = False

class Tile:
    # an object of this class represents a Rectangular Tile

    def __init__(self, x, y, width, height,surface):

        # Initialize a tile to contain a ' '
        # - x is the int x coord of the upper left corner
        # - y is the int y coord of the upper left corner
        # - width is the int width of the tile
        # - height is the int height of the tile
        # - surface is pygame.Surface object on which a Tile object is drawn on

        self.rect = pygame.Rect(x,y,width,height)
        self.surface = surface
        # New Instance Attribute
        self.content = ''
        self.flashing = False
    
    def set_flashing_on(self):
        self.flashing = True
    
    def equal(self,other_tile):
        if self.content != '' and self.content == other_tile.content:
            return True
        else:
            return False
    
    def draw(self):
        # draws a Tile object
        # -self is the Tile object to draw
        color = pygame.Color('white')
        border_width = 3
        if self.flashing == False:
            # 1. black rectangle with a white border
            # 2. draw the content of the tile
            pygame.draw.rect(self.surface,color,self.rect,border_width)
            self.draw_content()
        else:
            # draw a white rectangle
            pygame.draw.rect(self.surface,color,self.rect)
            self.flashing = False
    
    def draw_content(self):
        # draw the content of a Tile object
        # - self is the Tile object to draw
        font_size = self.surface.get_height()//3
        fg_color = pygame.Color('white')
        # create a font object
        font = pygame.font.SysFont('',font_size)
        # create a text_box
        text_box = font.render(self.content,True,fg_color)
        # compute the top left corner of the text_box
        # - text_box is a pygame.Surface object
        text_box_rect = text_box.get_rect()
        # - Set the center of the text_box_rect to the center of self.rect
        text_box_rect.center = self.rect.center
        # blit - draws the text_box onto the target surface
        # the text_box onto the target
        location = (text_box_rect.x,text_box_rect.y)
        self.surface.blit(text_box,location)
        #  self.surface.blit(text_box,text_box_rect) 

    def select(self,position,player):
        # return True if an unoccupied Tile is selected
        # return False if an occupied Tile is selected or no Tile is selected
        # - self is Tile to select
        # - position is a tuple that holds the (x,y) position of the mouse click
        # - player is of type str that represent the X or O player
        change_turn = False
        if self.rect.collidepoint(position):
            if self.content == '':
                self.content = player
                change_turn = True
            else:
                self.flashing = True
        return change_turn

main()