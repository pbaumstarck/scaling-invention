#!/usr/bin/env python3

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
  * board List[List[Int]]: This is all `None`s except for one zero where the knight is.

  Returns the board.
  """
  # Expand knights currently on this move count.
  move_count = 0
  while any(any(_ is None for _ in row) for row in board):
    for r in range(8):
      for c in range(8):
        if board[r][c] == move_count:
          # Mark all valid knight's moves from `(r, c)` with `move_count + 1`.
          for dr, dc in KNIGHT_MOVE_OFFSETS:
            rr = r + dr
            cc = c + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
              val = board[rr][cc]
              if val is None or move_count + 1 < val:
                board[rr][cc] = move_count + 1

    move_count += 1

  return board

max_max = 0
board_maxes = create_board()
for r in range(8):
  for c in range(8):
    board = create_board()
    board[r][c] = 0
    cover_with_knights_moves(board)
    render_board(board)

    board_max = max(max(row) for row in board)
    board_maxes[r][c] = board_max
    print(r, c, board_max)
    max_max = max(max_max, board_max)

print(max_max)
render_board(board_maxes)

