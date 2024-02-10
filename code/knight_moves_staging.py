
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm



def slide1():
  print('\nSlide')
  board = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
  ]
  print(board)


def slide2():
  print('\nSlide')
  board = [
    [None, None, None, None, None, None, None, None] for _ in range(8)
  ]
  print(board)


  board = [[None] * 8 for _ in range(8)]
  print(board)


def slide3():
  board = [[None] * 8 for _ in range(8)]

  def print_board(board):
    print('\n'.join(str(row) for row in board))

  print_board(board)


  def print_board(board):
    print('\n'.join(
      ''.join(str(_) for _ in row)
      for row in board
    ))

  print_board(board)


  def print_board(board):
    print('\n'.join(
      ''.join('_' if _ is None else str(_) for _ in row)
      for row in board
    ))

  print_board(board)


def print_board(board):
  print('\n'.join(
    ''.join('_' if _ is None else str(_) for _ in row)
    for row in board
  ))


def slide4():
  board = [[None] * 8 for _ in range(8)]

  r = c = 3
  board[r][c] = 0
  print('\nWith one knight:')
  print_board(board)

  board[r - 2][c - 1] = 1
  board[r - 1][c - 2] = 1
  board[r + 2][c - 1] = 1
  board[r + 1][c - 2] = 1
  board[r - 2][c + 1] = 1
  board[r - 1][c + 2] = 1
  board[r + 2][c + 1] = 1
  board[r + 1][c + 2] = 1

  print('\nKnight expanded:')
  print_board(board)


def slide4():
  board = [[None] * 8 for _ in range(8)]

  r = c = 3
  board[r][c] = 0
  print('\nWith one knight:')
  print_board(board)

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

  for dr, dc in KNIGHT_MOVE_OFFSETS:
    rdr = r + dr
    cdc = c + dc
    if 0 <= rdr < 8 and 0 <= cdc < 8:
      board[rdr][cdc] = 1

  print('\nKnight expanded:')
  print_board(board)


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

def slide5():
  board = [[None] * 8 for _ in range(8)]

  r = c = 3
  board[r][c] = 0
  print('\nWith one knight:')
  print_board(board)

  for move in range(2):
    for r in range(8):
      for c in range(8):
        if board[r][c] == move:
          for dr, dc in KNIGHT_MOVE_OFFSETS:
            rdr = r + dr
            cdc = c + dc
            if 0 <= rdr < 8 and 0 <= cdc < 8:
              board[rdr][cdc] = move + 1

  print('\nKnight expanded:')
  print_board(board)



def slide6():
  board = [[None] * 8 for _ in range(8)]

  r = c = 3
  board[r][c] = 0
  print('\nWith one knight:')
  print_board(board)

  for move in range(2):
    for r in range(8):
      for c in range(8):
        if board[r][c] == move:
          for dr, dc in KNIGHT_MOVE_OFFSETS:
            rdr = r + dr
            cdc = c + dc
            if 0 <= rdr < 8 and 0 <= cdc < 8 and board[rdr][cdc] is None:
              board[rdr][cdc] = move + 1

  print('\nKnight expanded:')
  print_board(board)


def slide7():
  board = [[None] * 8 for _ in range(8)]

  r = c = 3
  board[r][c] = 0
  print('\nWith one knight:')
  print_board(board)

  for move in range(10):
    for r in range(8):
      for c in range(8):
        if board[r][c] == move:
          for dr, dc in KNIGHT_MOVE_OFFSETS:
            rdr = r + dr
            cdc = c + dc
            if 0 <= rdr < 8 and 0 <= cdc < 8 and board[rdr][cdc] is None:
              board[rdr][cdc] = move + 1

  print('\nKnight expanded:')
  print_board(board)

  import numpy as np
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm
  fig, ax = plt.subplots()
  i = ax.imshow(np.array(board, dtype=np.float32), cmap=cm.jet, interpolation='nearest')
  fig.colorbar(i)
  plt.show()



def render_board(board):
  """Renders a board on a plot."""
  fig, ax = plt.subplots()
  i = ax.imshow(np.array(board, dtype=np.float32), cmap=cm.jet, interpolation='nearest')
  fig.colorbar(i)
  plt.show()



slide7()
