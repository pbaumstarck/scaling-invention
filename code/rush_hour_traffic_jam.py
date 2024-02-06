#!/usr/bin/env python

import random

N = 6
EMPTY_SPACE = '_'
ICE_CREAM_TRUCK = 'A'
START_ROW = 2


def get_board():
  # Uppercase is horizontal, lowercase is vertical.
  board = [[EMPTY_SPACE] * 6 for _ in range(N)]
  # Initialize the ice cream truck in a random column.
  start_col = random.randrange(N - 2)
  board[START_ROW][start_col] = board[START_ROW][start_col + 1] = ICE_CREAM_TRUCK

  # Add more cars.
  num_attempts = 0
  for i in range(random.randrange(6, 10)):
    car_len = random.randrange(2, 4)
    while True:
      vertical = random.randrange(2) == 0
      r = random.randrange(N - (car_len - 1) * int(vertical))
      c = random.randrange(N - (car_len - 1) * int(not vertical))
      is_clear = True
      for j in range(car_len):
        if board[r + j * int(vertical)][c + j * int(not vertical)] != EMPTY_SPACE:
          is_clear = False
          break

      if is_clear:
        car_char = chr(ord('b' if vertical else 'B') + i)
        for j in range(car_len):
          board[r + j * int(vertical)][c + j * int(not vertical)] = car_char
        break

      num_attempts += 1
      if num_attempts > 1000:
        # We have enough cars anyway.
        break

  return board


def board_str(board):
  return '\n'.join(''.join(_) for _ in board)


def copy_board(board):
  return [_[:] for _ in board]


def is_solved(board):
  # Find any obstacles between the ice cream truck and the right edge.
  for i in range(N - 1, -1, -1):
    char_i = board[START_ROW][i]
    if char_i == EMPTY_SPACE:
      continue
    elif char_i == ICE_CREAM_TRUCK:
      return True
    else:
      return False

  return True


def get_next_states(board):
  processed_chars_set = set([EMPTY_SPACE])
  next_states = []
  for r in range(N):
    for c in range(N):
      char = board[r][c]
      if char not in processed_chars_set:
        processed_chars_set.add(char)
        delta_r = 0
        delta_c = 0
        is_vertical = not char.isupper()
        if is_vertical:
          delta_r = 1
        else:
          delta_c = 1

        # Find the extrema
        min_r, max_r = r, r
        min_c, max_c = c, c
        while min_r - delta_r >= 0 and min_c - delta_c >= 0 and board[min_r - delta_r][min_c - delta_c] == char:
          min_r -= delta_r
          min_c -= delta_c

        while max_r + delta_r < N and max_c + delta_c < N and board[max_r + delta_r][max_c + delta_c] == char:
          max_r += delta_r
          max_c += delta_c

        if min_r - delta_r >= 0 and min_c - delta_c >= 0 and board[min_r - delta_r][min_c - delta_c] == EMPTY_SPACE:
          next_state = copy_board(board)
          next_state[min_r - delta_r][min_c - delta_c] = char
          next_state[max_r][max_c] = EMPTY_SPACE
          next_states.append(next_state)

        if max_r + delta_r < N and max_c + delta_c < N and board[max_r + delta_r][max_c + delta_c] == EMPTY_SPACE:
          next_state = copy_board(board)
          next_state[min_r][min_c] = EMPTY_SPACE
          next_state[max_r + delta_r][max_c + delta_c] = char
          next_states.append(next_state)

  return next_states


PLIES = {}
def search(board):
  queue = [(0, [board])]
  board_hash_set = set()

  while queue:
    ply, path = queue.pop(0)
    if ply not in PLIES:
      PLIES[ply] = 1
    else:
      PLIES[ply] += 1

    if is_solved(path[-1]):
      return path

    for next_state in get_next_states(path[-1]):
      if board_str(next_state) not in board_hash_set:
        board_hash_set.add(board_str(next_state))
        queue.append((ply + 1, path + [next_state]))

  return []

while True:
  board = get_board()
  path = search(board)
  print('Solved length: {}'.format(len(path)))
  print(PLIES)
  if len(path) >= 15:
    print('\n\n'.join(board_str(_) for _ in path))
    break
