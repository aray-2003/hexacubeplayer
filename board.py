# coding: utf-8

import sys, math, numpy as np

class Move:
  def __init__(self, piece, loc):
    self.piece = piece
    self.loc = loc

class Board:
  def __init__(self, moves):
    self.board = [
          [0,0,0,0,0],
         [0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
         [0,0,0,0,0,0],
          [0,0,0,0,0]
    ]

    self.cross_rows = [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]], [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]], [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]], [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7]], [[4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8]], [[5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7]], [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6]], [[7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5]], [[8, 0], [8, 1], [8, 2], [8, 3], [8, 4]], [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4]], [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 5], [6, 5], [7, 5]], [[0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 6], [6, 6]], [[0, 3], [1, 4], [2, 5], [3, 6], [4, 7], [5, 7]], [[0, 4], [1, 5], [2, 6], [3, 7], [4, 8]], [[1, 0], [2, 1], [3, 2], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3]], [[2, 0], [3, 1], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2]], [[3, 0], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]], [[4, 0], [5, 0], [6, 0], [7, 0], [8, 0]], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]], [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 0]], [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 1], [6, 0]], [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 2], [6, 1], [7, 0]], [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 3], [6, 2], [7, 1], [8, 0]], [[1, 5], [2, 5], [3, 5], [4, 5], [5, 4], [6, 3], [7, 2], [8, 1]], [[2, 6], [3, 6], [4, 6], [5, 5], [6, 4], [7, 3], [8, 2]], [[3, 7], [4, 7], [5, 6], [6, 5], [7, 4], [8, 3]], [[4, 8], [5, 7], [6, 6], [7, 5], [8, 4]]]

    self.score = 0
    self.score_last = 0
    self.spaces = 61

    # Iterate through all of the previous moves
    for move in moves:
      self.make_move(move)

  def key(self):
    return "".join(["".join([str(pos) for pos in row]) for row in self.board])

  def duplicate(self):
    b = Board([])
    b.board = [x[:] for x in self.board]
    b.score = self.score
    b.spaces = self.spaces
    return b

  # Get all valid moves
  def get_moves(self, pieces):
    valid = []
    for piece in pieces:
      for row in range(9):
        for pos in range(len(self.board[row])):
          if self.can_place_piece(piece, [row, pos]):
            valid.append(Move(piece, [row, pos]))
    return valid

  # Make a move
  def make_move(self, move):
    piece = move.piece
    loc = move.loc

    # Place the piece
    self.place_piece(piece, loc)

    # Check to see if any rows were completed (by the piece)
    rows = self.completed_rows(piece, loc)

    # Handles scoring
    score = 40 # for placing a piece
    if len(rows) > 0:
      base = 10 * (len(rows) + 1)
      for i, row in enumerate(rows):
        # Number of pieces * (base score * 1.2^row index)
        score += int(len(row) * (math.floor((base * max(1.2**i, 1)))))

    # Clears those rows
    for row in rows:
      self.clear_row(row)

    self.score_last = score
    self.score += score

  # Checks to see if there are any full rows
  # Rows are defined by a starting position, a direction, and a length (for calculation ease)
  def completed_rows(self, piece, loc):
    completed = []
    for row in self.cross_rows:
      is_finished = True
      for loc in row:
        if self.val(loc) == 0:
          is_finished = False
      if is_finished:
        completed.append(row)

    return completed

  # Places the piece on the board
  def place_piece(self, piece, loc):
    board = self.board

    self.spaces -= 1

    board[loc[0]][loc[1]] = piece.color
    for d in piece.path:
      self.spaces -= 1
      loc = self.next_loc(loc, d)
      board[loc[0]][loc[1]] = piece.color

  def clear_row(self, row):
    board = self.board

    for loc in row:
      board[loc[0]][loc[1]] = 0
      self.spaces += 1

  # Location helper
  def next_loc(self, loc, direction):
    b = 4

    if direction == 'l':
      return [loc[0], loc[1]-1]
    elif direction == 'r':
      return [loc[0], loc[1]+1]
    elif direction == 'ul':
      return [loc[0]-1, loc[1] - (0 if loc[0] > b else 1)]
    elif direction == 'ur':
      return [loc[0]-1, loc[1] + (0 if loc[0] <= b else 1)]
    elif direction == 'dl':
      return [loc[0]+1, loc[1] - (0 if loc[0] < b else 1)]
    elif direction == 'dr': 
      return [loc[0]+1, loc[1] + (0 if loc[0] >= b else 1)]

  # Tells you if you can place a piece in a certain location
  def can_place_piece(self, piece, loc):
    board = self.board
    try:
      if board[loc[0]][loc[1]] != 0:
        return False
      for d in piece.path:
        loc = self.next_loc(loc, d)
        if loc[0] < 0 or loc[1] < 0 or board[loc[0]][loc[1]] != 0:
          return False
    except Exception:
      return False
    return True

  '''
    Get the value at a specific location
  '''
  def val(self, loc):
    return self.board[loc[0]][loc[1]]

  '''
    Prints out the full board
  '''
  def print_self(self):
    board = self.board
    board_size = len(board)

    for row in board:
      sys.stdout.write(" " * (board_size + 1 - len(row)))
      for i in row:
        if i == 0: # empty
          sys.stdout.write("⬡ ")
        elif i == 1: # black
          sys.stdout.write("⬢ ")
        elif i == 2: # green
          sys.stdout.write('\033[92m' + "⬢ " + '\033[0m')
        elif i == 3: # magenta
          sys.stdout.write('\033[95m' + "⬢ " + '\033[0m')
        elif i == 4: # red
          sys.stdout.write('\033[91m' + "⬢ " + '\033[0m')
        elif i == 5: # yellow
          sys.stdout.write('\033[93m' + "⬢ " + '\033[0m')
        elif i == 6: # blue
          sys.stdout.write('\033[94m' + "⬢ " + '\033[0m')
      print("")