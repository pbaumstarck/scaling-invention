
def board2str(board):
  return '\n'.join(''.join(_) for _ in board)

board = [['.'] * 3, ['.'] * 3, ['.'] * 3]
print(board2str(board))
# ...
# ...
# ...

board[1][1] = 'x'
board[2][2] = 'o'
print(board2str(board))
# ...
# .x.
# ..o


# ======


def is_final_state(board):
  if sum(board[r][c] != '.' for r in range(3) for c in range(3)) == 9:
    # All spaces filled.
    return True

  for win in ('x', 'o'):
    # Check wins along a row.
    for r in range(3):
      if all(piece == win for piece in board[r]):
        return True

    # Check wins along a column.
    for c in range(3):
      if all(board[r][c] == win for r in range(3)):
        return True

    # Check diagonals.
    if board[0][0] == win and board[1][1] == win and board[2][2] == win:
      return True
    if board[0][2] == win and board[1][1] == win and board[2][0] == win:
      return True

  return False

print(is_final_state([
  list('...'),
  list('.x.'),
  list('..o'),
]))
# False
print(is_final_state([
  list('..x'),
  list('..x'),
  list('..x'),
]))
# True
print(is_final_state([
  list('o.x'),
  list('.ox'),
  list('..o'),
]))
# True
print(is_final_state([
  list('xoo'),
  list('oxx'),
  list('xxo'),
]))
# True


# ======


def next_states(board):
  next_piece = 'x' if sum(board[r][c] != '.' for r in range(3) for c in range(3)) % 2 == 0 else 'o'
  for r in range(3):
    for c in range(3):
      if board[r][c] == '.':
        next_board = [row.copy() for row in board]
        next_board[r][c] = next_piece
        yield next_board


for next_board in next_states([
  list('o.x'),
  list('.ox'),
  list('...'),
]):
  print('\n' + board2str(next_board))
#
# oxx
# .ox
# ...

# o.x
# xox
# ...

# o.x
# .ox
# x..

# o.x
# .ox
# .x.

# o.x
# .ox
# ..x


# ======


def dfs(board, valids):
  valids.append([row.copy() for row in board])
  if not is_final_state(board):
    for next_board in next_states(board):
      dfs(next_board, valids)

import time

board = [['.'] * 3 for _ in range(3)]
valids = []
start_time = time.time()
dfs(board, valids)
stop_time = time.time()
print('Num valids:', len(valids), 'took:', stop_time - start_time, 's')
# Num valids: 549946 took: 5.579200983047485 s


# ======


def dfs2(board, valids):
  board_str = board2str(board)
  if board_str not in valids:
    valids.add(board_str)
    if not is_final_state(board):
      for next_board in next_states(board):
        dfs2(next_board, valids)

import time

board = [['.'] * 3 for _ in range(3)]
valids = set()
start_time = time.time()
dfs2(board, valids)
stop_time = time.time()
print('Num valids:', len(valids), 'took:', stop_time - start_time, 's')
# Num valids: 5478 took: 0.10553789138793945 s


# ======


def dfs3(cells, valids):
  if len(cells) == 9:
    board = [cells[:3], cells[3:6], cells[6:]]
    if is_valid(board):
      valids.append([row.copy() for row in board])

  else:
    dfs3(cells + ['.'], valids)
    dfs3(cells + ['x'], valids)
    dfs3(cells + ['o'], valids)


def is_valid(board):
  return True

valids_exhaustive = []
dfs3([], valids_exhaustive)
print('Valids:', len(valids_exhaustive))
# Valids: 19683


# ======


def is_valid(board):
  num_xs = sum(sum(_ == 'x' for _ in row) for row in board)
  num_os = sum(sum(_ == 'o' for _ in row) for row in board)

  if (num_xs - num_os) not in (0, 1):
    return False

  return True

valids_xo = []
dfs3([], valids_xo)
print('X-O count valids:', len(valids_xo))
# Valids: 6046


# ======


def check_wins(board, win):
  win_positions = set()

  # Check wins along a row.
  for r in range(3):
    if all(piece == win for piece in board[r]):
      win_positions.update([(r, c) for c in range(3)])

  # Check wins along a column.
  for c in range(3):
    if all(board[r][c] == win for r in range(3)):
      win_positions.update([(r, c) for r in range(3)])

  # Check diagonals.
  if board[0][0] == win and board[1][1] == win and board[2][2] == win:
    win_positions.update([(0, 0), (1, 1), (2, 2)])
  if board[0][2] == win and board[1][1] == win and board[2][0] == win:
    win_positions.update([(0, 2), (1, 1), (2, 0)])

  return win_positions


def is_valid(board):
  num_xs = sum(sum(_ == 'x' for _ in row) for row in board)
  num_os = sum(sum(_ == 'o' for _ in row) for row in board)

  if (num_xs - num_os) not in (0, 1):
    return False

  x_wins = check_wins(board, 'x')
  o_wins = check_wins(board, 'o')
  if x_wins and o_wins:
    return False

  return True

valids_xo_double_win = []
dfs3([], valids_xo_double_win)
print('X-O count, no double wins valids:', len(valids_xo_double_win))
# X-O count, no double wins valids: 5890

print(set(map(board2str, valids_xo_double_win)) - valids)
# {'xxo\nxoo\nxo.', 'oxx\noxx\no..', 'oxo\n.x.\n.xo', '.x.\nox.\noxo',
# 'x.x\nooo\nxx.', '..o\nxxx\noo.', 'oo.\no..\nxxx', 'ooo\nxx.\n.xx',
# 'oox\noxo\nxx.', 'xxx\noo.\no..', '.ox\noxo\nx..', 'oox\noox\nx.x',
# '.xo\nxxo\nx.o', 'xoo\nx.o\nx..', 'oox\n.xx\nxoo', 'o.x\n.xo\nx.o', ...


# ======


def is_valid(board):
  num_xs = sum(sum(_ == 'x' for _ in row) for row in board)
  num_os = sum(sum(_ == 'o' for _ in row) for row in board)

  if (num_xs - num_os) not in (0, 1):
    return False

  x_wins = check_wins(board, 'x')
  o_wins = check_wins(board, 'o')
  if x_wins and o_wins:
    return False
  if x_wins and num_xs != num_os + 1:
    return False
  if o_wins and num_xs != num_os:
    return False

  return True

valids_xo_fixed_win = []
dfs3([], valids_xo_fixed_win)
print('X-O count, fixed win valids:', len(valids_xo_fixed_win))
# X-O count, fixed win valids: 5478


# ======


def pos2board(pos):
  c = lambda c: 'x' if c == 1 else ('o' if c == 2 else '.')
  return [
    [c(pos[0]), c(pos[1]), c(pos[2])],
    [c(pos[3]), c(pos[4]), c(pos[5])],
    [c(pos[6]), c(pos[7]), c(pos[8])],
  ]

valid_counting = set()
for i in range(3 ** 9):
  pos = []
  v = i
  for j in range(9):
    pos.append(i % 3)
    i = i // 3

  board = pos2board(pos)
  if is_valid(board):
    valid_counting.add(board2str(board))

print('Counting valids:', len(valid_counting))
# Counting valids: 5478
