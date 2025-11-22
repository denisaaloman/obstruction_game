from domain.board import Board
from gamecontroller.game import Game
from userinterface.ui import UI
from userinterface.settings import Settings

settings=Settings().printdim()
board=Board(settings.boardX, settings.boardY)
game=Game(board)
ui=UI(game)
ui.printgame()