from validators import *
from random import choice

class Game(object):
    def __init__(self, board):
        self._board=board
        self._valid=ValidateBoardDimensions()

    @property
    def board(self):
        return self._board

    def moveHuman(self,move):
        '''
        class method for human move
        we want to see if the move is valid
        then the move is made if no errors are raised
        '''
        self._valid.validatecoord(move.boardX,move.boardY,self._board)
        self._board.move('X',move)

    def evaluate(self, board):
        '''
        class method to evaluate a board position from the computer's perspective
        :param board (Board): the current board state to evaluate
        :return: an integer, a heuristic score for the board. Higher is better for the computer.
                Currently calculates the negative of the opponent's potential moves
                (less mobility for the opponent is better)
        '''
        # estimate opponent mobility after best response
        opponent_moves=0
        for move in board.emptysquares():
            temp=board.copy()
            temp.move('X', move)
            opponent_moves += len(temp.emptysquares())

        return -opponent_moves

    def ordered_moves(self, board):
        '''
        generate a list of valid moves ordered by "blocking power"
        :param board(Board): the current board state
        :return: list of Coordinates: a list of empty squares sorted
                 so that moves which block the most positions come first
        '''
        moves=[]
        for move in board.emptysquares():
            temp=board.copy()
            temp.move('O', move)
            blocked=len(board.emptysquares()) - len(temp.emptysquares())
            moves.append((blocked, move))

        moves.sort(reverse=True)  #most blocking first
        return [m[1] for m in moves]

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        '''
        :param
        board (Board): current board state.
        depth (int): how many moves ahead to simulate.
        alpha (float): alpha value for pruning (best already explored max).
        beta (float): beta value for pruning (best already explored min).
        is_maximizing (bool): True if it's the computer's turn (maximizing),
                              False if it's the human's turn (minimizing).
        :return: int: Heuristic score of the board for the computer. Positive = good for O.
        '''

        if board.iswon():
            return -1000 if is_maximizing else 1000

        if depth == 0:
            return self.evaluate(board)

        if is_maximizing:  #computer (O)
            value = -float('inf')
            for move in self.ordered_moves(board):
                new_board = board.copy()
                new_board.move('O', move)

                value = max(
                    value,
                    self.minimax(new_board,depth - 1,alpha,beta,False)
                )

                alpha=max(alpha, value)
                if alpha >= beta:
                    break
            return value

        else:  #human (X)
            value=float('inf')
            for move in board.emptysquares():
                new_board=board.copy()
                new_board.move('X', move)

                value=min(
                    value,
                    self.minimax(new_board, depth - 1, alpha, beta, True)
                )

                beta = min(beta,value)
                if alpha >= beta:
                    break
            return value

    def moveComputer(self):
        '''
        Choose the best move for the computer and apply it to the board.
        The method:
            Determines search depth based on board size
            Uses ordered moves and alpha–beta Minimax
            Picks the move with the best heuristic score
            Updates the board with the chosen move
        :param : None
        :return: None
        '''
        if self._board.width <= 3 and self._board.height <= 3:
            DEPTH = 9
        elif self._board.width <= 5:
            DEPTH = 4
        else:
            DEPTH = 2

        best_score=-float('inf')
        best_move=None

        for move in self.ordered_moves(self._board):
            temp_board=self._board.copy()
            temp_board.move('O', move)

            score=self.minimax(temp_board,DEPTH,-float('inf'),float('inf'),False)
            if score > best_score:
                best_score=score
                best_move=move
        self._board.move('O', best_move)

    def moveComputerSimpleLogic(self):
        '''
        class method that handles computer's move
        If the computer can win in its turn, then it makes the winning move
        If the human can win in its next round, then the computer blocks the move
        If these strategies cannot be applied, then a valid move is made
        '''

        #trying to see if the computer can win
        lempsquare=self._board.emptysquares()

        for square in lempsquare:
            board=self._board.copy()
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

