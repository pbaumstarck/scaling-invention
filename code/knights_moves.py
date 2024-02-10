#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def print_board(board):
  """Prints the board conveniently."""
  print('\n' + '\n'.join(
    [
      ''.join('_' if _ is None else str(_) for _ in row)
      for row in board
    ]
  ))


def create_board():
  """Creates a fresh 8x8 board filled with `None`s."""
  return [[None] * 8 for _ in range(8)]


def render_board(board):
  """Renders a board on a plot."""
  board_array = np.array(board, dtype=np.float32)
  fig, ax = plt.subplots()
  i = ax.imshow(board_array, cmap=cm.jet, interpolation='nearest')
  fig.colorbar(i)
  plt.show()


# List of the `(row, column)` offsets for all possible knight moves.
KNIGHT_MOVE_OFFSETS = [
  (2, 1),
  (1, 2),
  (-2, 1),
  (-1, 2),
  (2, -1),
  (1, -2),
  (-2, -1),
  (-1, -2),
]


def cover_with_knights_moves(board):
  """Cover a board by expanding a knight's moves.

  Args:
    board (List[List[Int]])

  Returns the board filled in with numbers.
  """
  while any(any(_ is None for _ in row) for row in board):
    for r in range(8):
      for c in range(8):
        move_count = board[r][c]
        if move_count is not None:
          # A knight got here in `move_count` moves, so mark all successor spaces with `move_count + 1`.
          for dr, dc in KNIGHT_MOVE_OFFSETS:
            rdr = r + dr
            cdc = c + dc
            if 0 <= rdr < 8 and 0 <= cdc < 8:
              target_val = board[rdr][cdc]
              if target_val is None or move_count + 1 < target_val:
                board[rdr][cdc] = move_count + 1

  return board

# board = create_board()
# render_board(board)

max_max = 0
board_maxes = create_board()
for r in range(4):
  for c in range(r, 4):
    board = create_board()
    board[r][c] = 0
    cover_with_knights_moves(board)
    # render_board(board)

    board_max = max(max(row) for row in board)
    board_maxes[r][c] = board_max
    print(r, c, board_max)
    max_max = max(max_max, board_max)

print(max_max)
render_board(board_maxes)


def reflect_board_(board):
  """Reflects the board in place.

  <=== c ==>
  +--------+ /\
  |        | r
  +--------+ \\/

  ==>

  <r>
  +-+
  | | /\
  | | c
  +-+ \\/

  Do operations on cells marked by 'X'.

  .XXXXXXX
  ..XXXXXX
  ...XXXXX
  ....XXXX
  .....XXX
  ......XX
  .......X
  ........

  """
  for r in range(len(board)):
    for c in range(r + 1, len(board)):
      board[c][r] = board[r][c]


reflect_board_(board_maxes)
render_board(board_maxes)


def rotate_board_(board):
  """

  <===== n ====>
  <== c ==>
  +-------+----+
  |       | r
  +-------+

  Location `(r, c)` copy to `(c, n - 1 r)`

          <==r=>
  +-------+----+ /\
          |    | ||
          |    | c
          |    | ||
          +----+ \\/

  """
  n = len(board)
  for r in range(math.floor(n / 2)):
    for c in range(math.floor(n / 2)):
      board[c][n - 1 - r] = board[r][c]

rotate_board_(board_maxes)
render_board(board_maxes)


def reflect_board_(board):
  n = len(board)
  for r in range(math.floor(n / 2)):
    for c in range(n):
      board[n - 1 - r][c] = board[r][c]

reflect_board_(board_maxes)
render_board(board_maxes)
