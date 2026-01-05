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



class TestEvaluate(unittest.TestCase):

    def setUp(self):
        self.board = Board(6, 6)
        self.game = Game(self.board)

    def test_empty_board(self):
        score = self.game.evaluate(self.board)
        self.assertEqual(score, -1040)

    def test_one_move(self):
        self.board.move('X', Coordinates(2, 2))
        score = self.game.evaluate(self.board)
        #Mobility decreases; score should be less negative
        self.assertLess(score, 0)
        self.assertGreater(score, -1040)  #less than full empty board

    def test_blocked_board(self):
        #Fill the board almost completely
        for i in range(6):
            for j in range(6):
                if i == 5 and j == 5:
                    continue
                self.board.move('X', Coordinates(i, j))
        score = self.game.evaluate(self.board)
        self.assertEqual(score,0)

class TestAI(unittest.TestCase):

    def setUp(self):
        self.board = Board(3, 3)
        self.game = Game(self.board)

    def test_ordered_moves(self):
        moves = self.game.ordered_moves(self.board)
        self.assertEqual(len(moves), 9)
        self.board.move('O', Coordinates(0, 0))
        moves_after = self.game.ordered_moves(self.board)
        for move in moves_after:
            self.assertNotEqual((move.boardX, move.boardY), (0, 0))
            self.assertNotEqual(self.board._board[move.boardX][move.boardY], 3)

        remaining_coords = [(m.boardX, m.boardY) for m in moves_after]
        expected_coords = [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertIn(remaining_coords[0], expected_coords)

    def test_minimax(self):
        self.board.move('O', Coordinates(0,0))
        self.board.move('O', Coordinates(0,1))
        self.board.move('X', Coordinates(1,0))
        self.board.move('X', Coordinates(1,1))

        #Evaluate minimax for the move at (0,2) (winning move)
        temp_board = self.board.copy()
        temp_board.move('O', Coordinates(0,2))
        score = self.game.minimax(temp_board, depth=3, alpha=-float('inf'), beta=float('inf'), is_maximizing=False)
        self.assertEqual(score, 1000)

    def test_move_computer(self):
        self.assertEqual(sum(val == 2 for row in self.board._board for val in row), 0)
        self.game.moveComputer()

        o_count = sum(val == 2 for row in self.board._board for val in row)
        self.assertEqual(o_count, 1)

        total = sum(val in [0, 2, 3] for row in self.board._board for val in row)
        self.assertEqual(total, 9)

        x_count = sum(val == 1 for row in self.board._board for val in row)
        self.assertEqual(x_count, 0)


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
        bd=self._game.board
        self.assertEqual(bd._board[2][3],1)
        self.assertEqual(bd._board[1][3],3)
        self.assertEqual(bd._board[5][7],0)
        move=Coordinates(2,3)
        self.assertRaises(CoordinateError,self._game.moveHuman,move)
    def testmovecomp(self):
        '''
        class method for testing if the computer made the move
        '''
        self._game.moveComputerSimpleLogic()
        bd=self._game.board
        self.assertLess(len(bd.emptysquares()),64)
        self.assertGreaterEqual(len(bd.emptysquares()),55)
    def testmovecompstrategy(self):
        '''
        class method for testing the strategies of the movement of the computer
        '''
        move=Coordinates(0,0)
        self._game2.moveHuman(move)
        self._game2.moveComputerSimpleLogic()
        bd=self._game2.board
        self.assertEqual(bd._board[2][2],2)
        self.assertEqual(bd._board[2][1],3)
        move=Coordinates(2,0)
        self._game2.moveHuman(move)
        self._game2.moveComputer()
        bd=self._game2.board
        self.assertEqual(bd._board[0][2],2)
