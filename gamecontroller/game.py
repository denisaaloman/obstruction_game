from validators import *
from random import choice

class Game(object):
    def __init__(self, board):
        self._board=board
        self._valid=ValidateBoardDimensions()

    def getboard(self):
        return self._board

    def moveHuman(self,move):
        '''
        class method for human move
        we want to see if the move is valid
        then the move is made if no errors are raised
        '''
        self._valid.validatecoord(move.boardX,move.boardY,self._board)
        self._board.move('X',move)


    def moveComputer(self):


        '''
        class method that handles computer's move
        If the computer can win in its turn, then it makes the winning move
        If the human can win in its next round, then the computer blocks the move
        If these strategies cannot be applied, then a valid move is made
        '''

        #trying to see if the computer can win
        lempsquare=self._board.emptysquares()

        for square in lempsquare:
            board = self._board.copy()
            board.move('O',square)
            if board.iswon() == True:
                self._board.move('O',square)
                return

        #blocking the next move for the human
        w=0
        for square in lempsquare:
            ok=0
            board=self._board.copy()
            board.move('O',square)
            newempty=board.emptysquares()
            for sq in newempty:
                    temp_board = board.copy()
                    temp_board.move('X',sq)
                    if temp_board.iswon() == True:
                        w=1
                        ok=1
            if ok==0 and w==1:
                self._board.move('O',square)
                return

        #if the previous strategies did not work, the computer makes a random valid move
        self._board.move('O', choice(lempsquare))



