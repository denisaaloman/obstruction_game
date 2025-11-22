class Coordinates:
    def __init__(self, boardX, boardY):
        '''
        class constructor, here we have the coordinates X and Y
        '''
        self._boardX = boardX
        self._boardY = boardY

    @property
    def boardX(self):
        return self._boardX
    @property
    def boardY(self):
        return self._boardY

    def __str__(self):
        '''
        overwrites the print method for the board coordinates
        '''
        return str(self._boardX) + ' ' + str(self._boardY)
