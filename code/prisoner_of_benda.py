#!/usr/bin/env python3

import heapq
import math


AMY = 0
BENDER = 1
BUBBLEGUM = 2
FARNSWORTH = 3
FRY = 4
HERMES = 5
LEELA = 6
NICOLAI = 7
SWEET_CLYDE = 8
WASHBUCKET = 9
ZOIDBERG = 10
NUM_CHARACTERS = 11

# CHARACTERS = [
#   AMY,
#   BENDER,
#   BUBBLEGUM,
#   FARNSWORTH,
#   FRY,
#   HERMES,
#   LEELA,
#   NICOLAI,
#   SWEET_CLYDE,
#   WASHBUCKET,
#   ZOIDBERG,
# ]

# `(body, mind)`
# state0 = [
#   (HERMES, AMY),
#   (LEELA, HERMES),
#   (FRY, ZOIDBERG),
#   (ZOIDBERG, FRY),
#   (FARNSWORTH, LEELA),
#   (NICOLAI, BENDER),
#   (WASHBUCKET, NICOLAI),
#   (AMY, WASHBUCKET),
#   (BENDER, FARNSWORTH),
#   (BUBBLEGUM, BUBBLEGUM),
#   (SWEET_CLYDE, SWEET_CLYDE),
# ]

# state0 = [
#   tuple(sorted((HERMES, AMY))),
#   tuple(sorted((LEELA, HERMES))),
#   tuple(sorted((FRY, ZOIDBERG))),
#   tuple(sorted((ZOIDBERG, FRY))),
#   tuple(sorted((FARNSWORTH, LEELA))),
#   tuple(sorted((NICOLAI, BENDER))),
#   tuple(sorted((WASHBUCKET, NICOLAI))),
#   tuple(sorted((AMY, WASHBUCKET))),
#   tuple(sorted((BENDER, FARNSWORTH))),
#   tuple(sorted((BUBBLEGUM, BUBBLEGUM))),
#   tuple(sorted((SWEET_CLYDE, SWEET_CLYDE))),
# ]
# state0.sort()
state0 = [None] * NUM_CHARACTERS
for body, mind in [
  # (HERMES, AMY),
  # (LEELA, HERMES),
  # (FRY, ZOIDBERG),
  # (ZOIDBERG, FRY),
  # (FARNSWORTH, LEELA),
  # (NICOLAI, BENDER),
  # (WASHBUCKET, NICOLAI),
  # (AMY, WASHBUCKET),
  # (BENDER, FARNSWORTH),
  # (BUBBLEGUM, BUBBLEGUM),
  # (SWEET_CLYDE, SWEET_CLYDE),
  (AMY, BENDER),
  (BENDER, AMY),
  (BUBBLEGUM, BUBBLEGUM),
  (FARNSWORTH, FARNSWORTH),
  (FRY, FRY),
  (HERMES, HERMES),
  (LEELA, LEELA),
  (NICOLAI, NICOLAI),
  (SWEET_CLYDE, SWEET_CLYDE),
  (WASHBUCKET, WASHBUCKET),
  (ZOIDBERG, ZOIDBERG),
]:
  state0[body] = mind

print(state0)

# denylist0 = [[False] * NUM_CHARACTERS for _ in range(NUM_CHARACTERS)]
# for body1, body2 in {
#   FARNSWORTH: AMY,
#   BENDER: AMY,
#   WASHBUCKET: AMY,
#   NICOLAI: WASHBUCKET,
#   LEELA: FARNSWORTH,
#   ZOIDBERG: FRY,
#   HERMES: LEELA,
# }.items():
#   denylist0[body1][body2] = True
#   denylist0[body2][body1] = True


def update_denylist(denylist, body1, body2):
  ix12 = body1 * NUM_CHARACTERS + body2
  ix21 = body2 * NUM_CHARACTERS + body1
  return denylist | (2 ** ix12) | (2 ** ix21)


def denylist_has(denylist, body1, body2):
  ix12 = body1 * NUM_CHARACTERS + body2
  return bool(denylist & (2 ** ix12))


denylist0 = 0  # [[False] * NUM_CHARACTERS for _ in range(NUM_CHARACTERS)]
for body1, body2 in [
  (FARNSWORTH, AMY),
  (BENDER, AMY),
  (WASHBUCKET, AMY),
  (NICOLAI, WASHBUCKET),
  (LEELA, FARNSWORTH),
  (ZOIDBERG, FRY),
  (HERMES, LEELA),
]:
  denylist0 = update_denylist(denylist0, body1, body2)
  # denylist0[body1][body2] = True
  # denylist0[body2][body1] = True


# print(denylist0)

cache = set()
cache.add(tuple(state0))


def get_heuristic(state):
  return 1

  # return max(1, math.ceil(0.5 * sum(_[0] != _[1] for _ in state)))
  # print(state)
  state_map = {i: state[i] for i in range(len(state))}
  cost = 0
  for body, mind in state_map.items():
    if body == mind or mind is None:
      continue

    body_ptr = body
    # state_map[body] = None
    num_iter = 0
    while state_map[body_ptr] != body:
      next_body_ptr = state_map[body_ptr]
      # print(body_ptr, next_body_ptr)
      state_map[body_ptr] = None
      body_ptr = next_body_ptr
      num_iter += 1

    state_map[body_ptr] = None
    cost += num_iter - 1
    # print('cost', cost, 'state_map', state_map)

  # breakpoint()
  return cost


print('first heuristic:', get_heuristic(state0))
print(state0)
i = 0
q = [(get_heuristic(state0), 0, state0, denylist0)]
# print(q)
while q:
  heuristic, cost, state, denylist = heapq.heappop(q)
  i += 1
  if i % 1000 == 0 or True:
    print(i, 'heur', heuristic, 'cost', cost, denylist, state)

  if all(state[i] == i for i in range(len(state))):
    print('Done!', state, denylist)
    break

  for body1 in range(len(state)):
    mind1 = state[body1]
    for body2 in range(len(state)):
      if body1 == body2:
        continue

      mind2 = state[body2]
      # print(body1, mind1, body2, mind2, denylist[body1][body2])
      # if not denylist[body1][body2]:
      if not denylist_has(denylist, body1, body2):
        new_state = state[:]
        new_state[body1], new_state[body2] = mind2, mind1
        new_state_tuple = tuple(new_state)
        if new_state_tuple not in cache:
          cache.add(new_state_tuple)
          # new_denylist = [_.copy() for _ in denylist]
          # new_denylist[body1][body2] = True
          # new_denylist[body2][body1] = True
          heapq.heappush(
            q,
            (
              cost + 1 + get_heuristic(new_state),
              cost + 1,
              new_state,
              update_denylist(denylist, body1, body2),
            ),
          )

  # print(q)
  # break




# 200000 4 5 12 [(1, 2), (2, 1), (3, 4), (4, 8), (5, 11), (6, 3), (7, 5), (8, 10), (9, 9), (10, 7), (11, 6)]
# 201000 4 5 12 [(1, 2), (2, 1), (3, 8), (4, 5), (5, 11), (6, 4), (7, 3), (8, 10), (9, 9), (10, 6), (11, 7)]
# 202000 4 5 12 [(1, 2), (2, 1), (3, 11), (4, 7), (5, 6), (6, 4), (7, 9), (8, 10), (9, 3), (10, 8), (11, 5)]
# 203000 4 5 12 [(1, 2), (2, 3), (3, 4), (4, 7), (5, 8), (6, 1), (7, 10), (8, 6), (9, 11), (10, 9), (11, 5)]
