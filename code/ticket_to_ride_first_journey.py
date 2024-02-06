
import json

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


def prims_algorithm(graph):
  vertices = graph.keys()

  C = {v: float('Inf') for v in vertices}
  E = {v: None for v in vertices}

  F = set()
  Q = set(vertices)

  while Q:
    v = list(sorted([(C[v], v) for v in Q]))[0][1]
    Q.remove(v)

    F.add(v)

    for w, vw in graph[v].items():
      if w in Q and vw < C[w]:
        C[w] = vw
        E[w] = v

  return E


# Create nested map of vertex-to-vertex edge weights.
graph = {v: {} for v in VERTICES}
for vertex1, vertex2, cost in EDGES:
  graph[vertex1][vertex2] = cost
  graph[vertex2][vertex1] = cost

E = prims_algorithm(graph)
print(json.dumps(E, indent=2))
print(sum(graph[v1][v2] for v1, v2 in E.items() if v2))
