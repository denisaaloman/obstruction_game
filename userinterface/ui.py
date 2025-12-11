import pygame
from pygame.locals import *
from domain.coordinates import Coordinates
from gamecontroller.game import Game
from domain.board import Board
from settings import Settings

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
CELL_SIZE = 60  #pixels

class ObstructionGUI:
    def __init__(self, game):
        self.game = game
        self.board = game.getboard()
        self.rows = self.board.height
        self.cols = self.board.width
        pygame.init()
        self.screen = pygame.display.set_mode((self.cols * CELL_SIZE, self.rows * CELL_SIZE + 50))
        pygame.display.set_caption("Obstruction Game")
        self.font = pygame.font.SysFont(None, 36)
        self.human_turn = True
        self.running = True

    def draw_board(self):
        self.screen.fill(WHITE)
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 2)
                val = self.board._board[r][c]
                if val == 1:
                    pygame.draw.circle(self.screen, BLUE, rect.center, CELL_SIZE // 2 - 5)
                elif val == 2:
                    pygame.draw.circle(self.screen, RED, rect.center, CELL_SIZE // 2 - 5)
                elif val == 3:
                    pygame.draw.rect(self.screen, GRAY, rect)

        status_text = "Human's Turn (X)" if self.human_turn else "Computer's Turn (O)"
        text_surf = self.font.render(status_text, True, BLACK)
        self.screen.blit(text_surf, (10, self.rows * CELL_SIZE + 10))
        pygame.display.flip()

    def get_cell_from_mouse(self, pos):
        x, y = pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        if row < self.rows and col < self.cols:
            return Coordinates(row, col)
        return None

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN and self.human_turn:
                    coord = self.get_cell_from_mouse(pygame.mouse.get_pos())
                    if coord:
                        try:
                            self.game.moveHuman(coord)
                            self.human_turn = False
                            if self.board.iswon():
                                self.draw_board()
                                pygame.time.wait(1000)
                                print("Human wins!")
                                self.running = False
                        except Exception as e:
                            print(e)

            if not self.human_turn and not self.board.iswon():
                pygame.time.wait(500)
                self.game.moveComputer()
                self.human_turn = True
                if self.board.iswon():
                    self.draw_board()
                    pygame.time.wait(1000)
                    print("Computer wins!")
                    self.running = False

            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    # Get board size
    s = Settings()
    coords = s.printdim()
    board = Board(coords.boardX, coords.boardY)
    game = Game(board)
    gui = ObstructionGUI(game)
    gui.run()

"""

from domain.board import Board
from validators import *
from domain.coordinates import Coordinates
from gamecontroller.game import Game


class UI:
    def __init__(self,game):
        self._game=game

    def makemove(self):
        while True:
            try:
                print("The move must have this format: <x> <space> <y>")
                coord=input().split(' ')
                return Coordinates(int(coord[0]),int(coord[1]))
            except ValueError:
                print("Invalid format. The input must be of the format: <x> <space> <y>")
            except IndexError:
                print("Invalid format. The input must be of the format: <x> <space> <y>")

    def printgame(self):
        print("Human starts!")
        human=True
        board=self._game.getboard()
        print(board)
        while not board.iswon():
            if human:
                move=self.makemove()

                try:
                    self._game.moveHuman(move)
                    print("Human has made its move. Board now is:")
                    print(board)
                    human = False
                except CoordinateError as cord:
                    print(cord)
            else:
                self._game.moveComputer()
                human=True
                print("Computer has made its move. Board now is:")
                print(board)
        print("\033[1;35m GAME OVER!")
        print(board)
        if human:
                print("\033[1;31m Computer has won!")
        else:
                print("\033[1;36m Human has won!")

"""



