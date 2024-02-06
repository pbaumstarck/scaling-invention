#!/usr/bin/env python

import copy

# TODO: Make this not a global variable.
N = 1

def toggle(board, r, c):
  """Toggles the state of the board given a click at `(r, c)`."""
  board[r][c] ^= 1

  if r:
    board[r - 1][c] ^= 1

  if r < N - 1:
    board[r + 1][c] ^= 1

  if c:
    board[r][c - 1] ^= 1

  if c < N - 1:
    board[r][c + 1] ^= 1


def toggles_str(toggles):
  """Converts a list of toggles to a newline-joined string."""
  return '\n'.join(''.join(_) for _ in toggles)


def rotate(matrix):
  """Rotates the matrix clockwise 90 degrees."""
  n = len(matrix)
  out_matrix = [[None] * n for _ in range(n)]
  for r in range(n):
    for c in range(n):
      out_matrix[r][c] = matrix[n - 1 - c][r]

  return out_matrix


def do_search(board, toggles, r, c, solutions, hashes):
  """Search for a solution on the board.

  Args:
  board List[List[str]]: The state of the board.
  toggles List[List[str]]: Whether we have toggled a position or not.
  r int: The current row to examine.
  c int: The current column to examine.
  solutions List[Toggles]: If passed in, a list to collect solutions in.
  hashes set[str]: A hash of all board solutions that have been saved.

  Returns bool: Whether a solution has been found.
  """
  if all(all(_) for _ in board):
    # Board is solved.
    if solutions is not None:
      # We are supposed to generate a list of all solutions.
      copy_toggles = copy.deepcopy(toggles)
      sol_hashes = set()
      for i in range(4):
        sol_hashes.add(toggles_str(copy_toggles))
        copy_toggles = rotate(copy_toggles)

      if not(hashes & sol_hashes):
        solutions.append(copy_toggles)
        hashes.update(sol_hashes)
    else:
      return True

  if r >= N or c >= N:
    return False

  if r and c and not board[r - 1][c - 1]:
    return False
  elif c == 0 and r > 1 and not board[r - 2][N - 1]:
    return False

  r_next = r
  c_next = c + 1
  if c_next >= N:
    r_next += 1
    c_next = 0

  # Try toggling.
  toggle(board, r, c)
  toggles[r][c] = '*'
  found = do_search(board, toggles, r_next, c_next, solutions, hashes)
  if found and solutions is None:
    return True
  toggles[r][c] = '.'
  toggle(board, r, c)

  # Try not toggling.
  return do_search(board, toggles, r_next, c_next, solutions, hashes)


# Find first solutions.
if False:
  for N in range(4, 20):
    board = [[0] * N for _ in range(N)]
    toggles = [['.'] * N for _ in range(N)]
    result = do_search(board, toggles, 0, 0, None, None)
    print('\nN: {}'.format(N))
    print('\n'.join(''.join(_) for _ in toggles))

# Find all solutions.
if True:
  for N in range(4, 20):
    board = [[0] * N for _ in range(N)]
    toggles = [['.'] * N for _ in range(N)]
    solutions = []
    hashes = set()
    do_search(board, toggles, 0, 0, solutions, hashes)
    print('\nN={} has {} solution(s):'.format(N, len(solutions)))
    for solution in solutions:
      print(toggles_str(solution) + '\n')
