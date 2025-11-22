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
class GUI:
    def __init__(self,game):
        self._game=game
        self.width=600
        self.height=600
        self.cell_size = 100
        self.colors = {
            'background': (255, 255, 255),
            'line': (0, 0, 0),
            'human': (0, 255, 0),
            'computer': (255, 0, 0)
        }
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Obstruction Game")
"""



