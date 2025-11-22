import unittest
from domain.board import Board
from gamecontroller.game import Game
from domain.coordinates import Coordinates
from validators import *

class TestBoard(unittest.TestCase):

    def setUp(self):
        '''
        setting the board
        '''
        self._board=Board(8,8)

    def testinit(self):
        '''
        class method for testing if the board is correctly initialized
        '''
        width=self._board.width
        height=self._board.height
        for i in range(8):
            for j in range(8):
                self.assertEqual(self._board._board[i][j],0)

    def testmove(self):
        '''
        class method for testing whether the move has been marked correctly
        '''
        coord=Coordinates(2,3)
        self._board.move('X',coord)
        self.assertEqual(self._board._board[1][3],3)
        self.assertEqual(self._board._board[0][3],0)
        self.assertEqual(self._board._board[2][3],1)
        self.assertEqual(self._board._board[3][4],3)

    def testemptysquares(self):
        '''
        class method for testing if there is the correct number of empty squares
        '''
        coord = Coordinates(2, 3)
        self._board.move('X', coord)
        l=self._board.emptysquares()
        self.assertNotEqual(l,[])
        self.assertEqual(len(l),55) #64-8-1
        self.assertNotEqual(len(l),64)

    def testwin(self):
        '''
        class method for testing if the game is won
        '''
        new_board=Board(3,3)
        new_board.move('X',Coordinates(1,1))
        nr=new_board.iswon()
        self.assertNotEqual(nr,[])
        self.assertNotEqual(nr,False)
        self.assertEqual(nr,True)
    def testcopy(self):
        coord = Coordinates(2, 3)
        self._board.move('X', coord)
        b2=self._board.copy()
        self.assertNotEqual(b2,None)
        self.assertEqual(b2.width,8)
        self.assertEqual(b2.height,8)
        self.assertNotEqual(b2._board,self._board)
        self.assertEqual(b2._board[2][3],1)


class TestValidation(unittest.TestCase):
    def setUp(self):
        self._board=Board(8,8)
        self._validator=ValidateBoardDimensions()

    def testdim(self):
        '''
        class method for testing if the board dimensions are correct
        '''
        width=self._board.width
        height=self._board.height
        self.assertRaises(BoardError,self._validator.validate,-2,-1)


    def testcoord(self):
        '''
        class method for testing if the board coordinates are correctly
        '''
        self.assertRaises(CoordinateError,self._validator.validatecoord,9,10,self._board)
        self.assertRaises(CoordinateError,self._validator.validatecoord,8,8,self._board)
        self._board.move('X',Coordinates(2,3))
        self.assertRaises(CoordinateError,self._validator.validatecoord,1,3,self._board)


class TestGame(unittest.TestCase):
    def setUp(self):
        self._board=Board(8,8)
        self._strategy_board=Board(3,3)
        self._game=Game(self._board)
        self._game2=Game(self._strategy_board)
    def testmovehuman(self):
        '''
        class method for testing the human move
        '''
        move=Coordinates(2,3)
        self._game.moveHuman(move)
        bd=self._game.getboard()
        self.assertEqual(bd._board[2][3],1)
        self.assertEqual(bd._board[1][3],3)
        self.assertEqual(bd._board[5][7],0)
        move=Coordinates(2,3)
        self.assertRaises(CoordinateError,self._game.moveHuman,move)
    def testmovecomp(self):
        '''
        class method for testing if the computer made the move
        '''
        self._game.moveComputer()
        bd=self._game.getboard()
        self.assertLess(len(bd.emptysquares()),64)
        self.assertGreaterEqual(len(bd.emptysquares()),55)
    def testmovecompstrategy(self):
        '''
        class method for testing the strategies of the movement of the computer
        '''
        move=Coordinates(0,0)
        self._game2.moveHuman(move)
        self._game2.moveComputer()
        bd=self._game2.getboard()
        self.assertEqual(bd._board[2][2],2)
        self.assertEqual(bd._board[2][1],3)
        move=Coordinates(2,0)
        self._game2.moveHuman(move)
        self._game2.moveComputer()
        bd=self._game2.getboard()
        self.assertEqual(bd._board[0][2],2)

















