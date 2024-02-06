#!/usr/bin/env python3

import copy
import json
import sys

from collections import defaultdict


# Initialize city names.
ALBUQUERQUE = 'Albuquerque'
ATLANTA = 'Atlanta'
CALGARY = 'Calgary'
CHICAGO = 'Chicago'
DALLAS = 'Dallas'
DENVER = 'Denver'
DULUTH = 'Duluth'
HELENA = 'Helena'
KANSAS_CITY = 'Kansas City'
LOS_ANGELES = 'Los Angeles'
MIAMI = 'Miami'
MONTREAL = 'Montreal'
NEW_ORLEANS = 'New Orleans'
NEW_YORK = 'New York'
SALT_LAKE_CITY = 'Salt Lake City'
SAN_FRANCISCO = 'San Francisco'
SEATTLE = 'Seattle'
WASHINGTON = 'Washington'
WINNIPEG = 'Winnipeg'

# Save list of vertices.
VERTICES = [
  ALBUQUERQUE,
  ATLANTA,
  CALGARY,
  CHICAGO,
  DALLAS,
  DENVER,
  DULUTH,
  HELENA,
  KANSAS_CITY,
  LOS_ANGELES,
  MIAMI,
  MONTREAL,
  NEW_ORLEANS,
  NEW_YORK,
  SALT_LAKE_CITY,
  SAN_FRANCISCO,
  SEATTLE,
  WASHINGTON,
  WINNIPEG,
]

# Save list of edges.
EDGES = [
  (SEATTLE, CALGARY, 3),
  (SEATTLE, HELENA, 2),
  (SEATTLE, SALT_LAKE_CITY, 3),
  (SEATTLE, SAN_FRANCISCO, 3),
  (CALGARY, WINNIPEG, 3),
  (CALGARY, HELENA, 1),
  (WINNIPEG, DULUTH, 1),
  (WINNIPEG, HELENA, 3),
  (DULUTH, MONTREAL, 3),
  (DULUTH, CHICAGO, 1),
  (DULUTH, KANSAS_CITY, 2),
  (DULUTH, DENVER, 4),
  (MONTREAL, NEW_YORK, 1),
  (MONTREAL, CHICAGO, 3),
  (NEW_YORK, WASHINGTON, 1),
  (NEW_YORK, CHICAGO, 3),
  (WASHINGTON, MIAMI, 4),
  (WASHINGTON, CHICAGO, 3),
  (WASHINGTON, ATLANTA, 2),
  (MIAMI, ATLANTA, 2),
  (MIAMI, NEW_ORLEANS, 3),
  (ATLANTA, CHICAGO, 2),
  (ATLANTA, NEW_ORLEANS, 1),
  (ATLANTA, DALLAS, 3),
  (ATLANTA, KANSAS_CITY, 3),
  (NEW_ORLEANS, DALLAS, 2),
  (CHICAGO, KANSAS_CITY, 1),
  (KANSAS_CITY, DENVER, 2),
  (KANSAS_CITY, DALLAS, 1),
  (DALLAS, ALBUQUERQUE, 2),
  (ALBUQUERQUE, DENVER, 1),
  (ALBUQUERQUE, LOS_ANGELES, 3),
  (ALBUQUERQUE, SALT_LAKE_CITY, 2),
  (SALT_LAKE_CITY, DENVER, 2),
  (SALT_LAKE_CITY, LOS_ANGELES, 2),
  (SALT_LAKE_CITY, SAN_FRANCISCO, 2),
  (SALT_LAKE_CITY, HELENA, 1),
  (DENVER, HELENA, 2),
  (SAN_FRANCISCO, LOS_ANGELES, 1),
]

# Save the list of 32 ticket cards.
TICKETS = [
  (CALGARY, CHICAGO),   # 0
  (CALGARY, LOS_ANGELES),  # 1
  (CALGARY, SAN_FRANCISCO),  # 2
  (CHICAGO, ALBUQUERQUE),  # 3
  (CHICAGO, MIAMI),  # 4 --
  (CHICAGO, NEW_ORLEANS),  # 5 --
  (DALLAS, MIAMI),   # 6
  (DENVER, LOS_ANGELES),   # 7
  (DENVER, NEW_ORLEANS),   # 8
  (DENVER, SAN_FRANCISCO),   # 9
  (DULUTH, ALBUQUERQUE),   # 10
  (DULUTH, SALT_LAKE_CITY),  # 11
  (DULUTH, WASHINGTON),  # 12
  (HELENA, CHICAGO),   # 13
  (HELENA, KANSAS_CITY),   # 14
  (KANSAS_CITY, MIAMI),  # 15
  (LOS_ANGELES, DALLAS),   # 16
  (MONTREAL, ATLANTA),   # 17
  (MONTREAL, KANSAS_CITY),   # 18
  (NEW_YORK, ATLANTA),   # 19 --
  (NEW_YORK, DALLAS),  # 20
  (NEW_YORK, MIAMI),   # 21 --
  (NEW_YORK, NEW_ORLEANS),   # 22 --
  (SALT_LAKE_CITY, DALLAS),  # 23
  (SEATTLE, ALBUQUERQUE),  # 24
  (SEATTLE, DENVER),   # 25
  (SEATTLE, LOS_ANGELES),  # 26
  (SEATTLE, WINNIPEG),   # 27
  (WASHINGTON, KANSAS_CITY),   # 28
  (WASHINGTON, NEW_ORLEANS),   # 29 --
  (WINNIPEG, MONTREAL),  # 30
  (WINNIPEG, NEW_YORK),  # 31
]

# Create nested map of vertices to vertices to edge weights.
graph = {v: {} for v in VERTICES}
for vertex1, vertex2, cost in EDGES:
  graph[vertex1][vertex2] = cost
  graph[vertex2][vertex1] = cost


def bellman_ford_algorithm(graph, source):
  vertices = graph.keys()
  distances = {_: float('Inf') for _ in vertices}
  predecessors = {_: None for _ in vertices}
  distances[source] = 0

  for i in range(len(vertices)):
    for u, edges in graph.items():
      for v, w in edges.items():
        if distances[u] + w < distances[v]:
          distances[v] = distances[u] + w
          predecessors[v] = u

  return distances, predecessors


def get_all_shortest_paths(graph):
  vertices = graph.keys()
  shortest_paths = {_: {__: ([], 0) for __ in vertices} for _ in vertices}
  for source in vertices:
    _, predecessors = bellman_ford_algorithm(graph, source)
    for sink in vertices:
      node = sink
      path = [node]
      weight = 0
      while node != source:
        previous_node = predecessors[node]
        weight += graph[previous_node][node]
        path.append(previous_node)
        node = previous_node

      shortest_paths[source][sink] = (path, weight)

  return shortest_paths


def kruskals_algorithm(graph, shortest_paths, terminals):
  F = [
    (0.0, [_]) for _ in terminals
  ]
  while len(F) > 1:
    # Shortest path represented as: `(weight, path, i, j)`
    shortest_path = (float('Inf'), None, None, None)
    for i in range(len(F) - 1):
      for j in range(i + 1, len(F)):
        for node_i in F[i][1]:
          for node_j in F[j][1]:
            path, weight = shortest_paths[node_i][node_j]
            if weight < shortest_path[0]:
              shortest_path = (weight, path, i, j)

    # Cut `i` and `j` out of `F`, and add the new merged `path`.
    weight, path, i, j = shortest_path
    F = (
      F[:i] + F[i + 1:j] + F[j + 1:] +
      [(
        F[i][0] + F[j][0] + weight,
        list(set(path + F[i][1] + F[j][1]))
      )]
    )

  return list(F[0])


shortest_paths = get_all_shortest_paths(graph)
n = len(TICKETS)
optimal_solutions = 0
for ix1 in range(n - 5):
  print('ix1:', ix1, '/', n - 5)
  for ix2 in range(ix1 + 1, n - 4):
    for ix3 in range(ix2 + 1, n - 3):
      for ix4 in range(ix3 + 1, n - 2):
        for ix5 in range(ix4 + 1, n - 1):
          for ix6 in range(ix5 + 1, n):
            terminals = list(set(
              TICKETS[ix1] +
              TICKETS[ix2] +
              TICKETS[ix3] +
              TICKETS[ix4] +
              TICKETS[ix5] +
              TICKETS[ix6]
            ))

            kruskal = kruskals_algorithm(graph, shortest_paths, terminals)
            if kruskal[0] == 8:
              # Print out an optimal hand.
              print('\nFound an optimal hand:')
              print(json.dumps([
                TICKETS[ix1],
                TICKETS[ix2],
                TICKETS[ix3],
                TICKETS[ix4],
                TICKETS[ix5],
                TICKETS[ix6],
              ], indent=2))
              optimal_solutions += 1

print('\nFound %d optimal solutions!' % optimal_solutions)
