from validators import *
from domain.coordinates import Coordinates

class Settings:
    def __init__(self):
        self._boardvalidator=ValidateBoardDimensions()

    def printdim(self):
       while True:
        print("Choose the board size!")
        h=input("Board height: ")
        w=input("Board width: ")
        try:
            h=int(h)
            w=int(w)
            self._boardvalidator.validate(h,w)
            return Coordinates(h,w)
        except ValueError:
            print("The dimensions of the board are invalid! Please enter positive integers.")
        except BoardError as e:
            print(e)