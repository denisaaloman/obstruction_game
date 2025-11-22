class BoardError(Exception):
    pass
class CoordinateError(Exception):
    pass

class ValidateBoardDimensions:

    def validate(self, height, width):
        '''
        class method to validate board dimensions
        if the dimensions are not positive, an error is raised
        '''
        if height<=0 or width<=0:
            raise BoardError("The dimensions of the board must be positive integers. Try again!")

    def validatecoord(self, x, y, board):
        '''
        class method to validate board coordinates
        x and y must not be outside the board' s dimensions
        '''
        errors=""
        if x<0 or y<0 or x>=board.height or y>=board.width:
            errors+="The coordinates of the board must be bewtween 0 and height/width-1. Try again!"
        if errors!="":
            raise CoordinateError(errors)
        if board._board[x][y]!=0:
            errors+="This square is taken! Choose an empty square, please!"
        if errors!="":
            raise CoordinateError(errors)





