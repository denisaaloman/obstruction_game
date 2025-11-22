from texttable import Texttable
import copy
from domain.coordinates import Coordinates

class Board:

    def __init__(self, height, width):
        '''
        class constructor, the board is initialized (width, height)
        '''
        self._width = width
        self._height = height
        self._board=[[0 for x in range(width)] for y in range(height)]
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __str__(self):
        '''
        class method to overwrite the print method
        '''
        table=Texttable()
        header=[' ']
        for index in range(self._width):
            header.append(str(index))
        table.header(header)
        data={0:" ",1:"X",2:"O",3:"#"}
        for rowindex in range(self._height):
            list=[rowindex]
            for colindex in range(self._width):
                list.append(data[self._board[rowindex][colindex]])
            table.add_row(list)
        return table.draw()

    def emptysquares(self):
        '''
        class method that returns a list of empty squares from the board
        '''
        emp=[]
        for i in range(self._height):
            for j in range(self._width):
                if self._board[i][j] == 0:
                    emp.append(Coordinates(i,j))
        return emp

    def iswon(self):
        '''
        class method that checks if the game is won
        '''
        return len(self.emptysquares())==0


    def copy(self):
      '''
      class method that returns a copy of the current board
      '''
      board=Board(self._height,self._width)
      board._board=copy.deepcopy(self._board)
      return board

    def move(self, symbol, coordinates):
        '''
        class method that handles moving a symbol to the coordinates (x,y)
        in- coordinates - (x,y) point on the board
            symbol - X or 0
        return: none
        '''
        symbols={'X':1,'O':2}
        coordX=coordinates.boardX
        coordY=coordinates.boardY
        self._board[coordX][coordY]=symbols[symbol]
        forRowIndex = [-1, -1, -1, 0, 1, 1, 1, 0]
        forColumnIndex = [-1, 0, 1, 1, 1, 0, -1, -1]
        for index in range(0, 8):
            if coordX + forRowIndex[index] >= 0 and coordX + forRowIndex[index] < self._height and coordY + forColumnIndex[index] >= 0 and coordY + forColumnIndex[index] < self._width:
                self._board[coordX + forRowIndex[index]][coordY + forColumnIndex[index]] = 3

