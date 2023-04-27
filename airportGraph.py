from route import Route


class AirportGraph:

  def __init__(self):
    self.adjacencyList = {}
#adds the routes
  def addRoute(self, route):
    #checks to see if airport 1 already exists or not
    if not (route.airport1 in self.adjacencyList.keys()):
      empty_list = []
      self.adjacencyList[route.airport1] = empty_list
#checks to see if airport 2 already exists or not
    if not (route.airport2 in self.adjacencyList.keys()):
      empty_list = []
      self.adjacencyList[route.airport2] = empty_list

    self.adjacencyList[route.airport1].append((route.airport2, route.distance))

  #the implementation of Dijkstra's algorithm
  def find_shortest_path_dijkstra(self, start, end):
    dijkstra_table = {}
    needs_processing = []
    computed = []

    #iterates through each airport in the adjacency list
    for airport in self.adjacencyList.keys():
      dijkstra_table[airport] = [float('inf'), None]
      needs_processing.append(airport)

    dijkstra_table[start] = [0, None]

    #checks whether the needs processing list is empty
    while len(needs_processing) > 0:

      #finds minimum distance in needs processing
      u = needs_processing[0]
      for airport in needs_processing:
        if (dijkstra_table[airport][0] < dijkstra_table[u][0]):
          u = airport

      #removes the minimum distance airport from needs processing and adds to computed
      needs_processing.remove(u)
      computed.append(u)

      #relaxes the each edge if it satisfies the conditions of Dijkstra's algorithm
      for pairElement in self.adjacencyList[u]:
        v = pairElement[0]
        weightUV = pairElement[1]

        if (v in needs_processing):
          if (dijkstra_table[u][0] + weightUV < dijkstra_table[v][0]):
            dijkstra_table[v][0] = dijkstra_table[u][0] + weightUV
            dijkstra_table[v][1] = u

    #crafts a route from the final table from Dijkstra's algorithm
    previous = end
    path = [previous]
    distance = dijkstra_table[end][0]

    #returns the route and distance
    while (previous != start):
      previous = dijkstra_table[previous][1]
      if (previous == None):
        return None, float('inf')
      path.insert(0, previous)

    return path, distance

  def find_shortest_path_bellman_ford(self, start, end):
    # Initialize distances and predecessors for all airports
    distances = {airport: float('inf') for airport in self.adjacencyList}
    predecessors = {airport: None for airport in self.adjacencyList}
    distances[start] = 0

    # Relax edges repeatedly
    num_airports = len(self.adjacencyList)
    i = 0
    while i < num_airports - 1:
      # Loop through each airport and its edges
      j = 0
      while j < num_airports:
        u = list(self.adjacencyList.keys())[j]
        k = 0
        while k < len(self.adjacencyList[u]):
          v, weight = self.adjacencyList[u][k]
          # Update distances and predecessors if shorter path found
          if distances[u] + weight < distances[v]:
            distances[v] = distances[u] + weight
            predecessors[v] = u
          k = k + 1
        j = j + 1
      i = i + 1

    # Check for negative-weight cycles
    j = 0
    while j < num_airports:
      u = list(self.adjacencyList.keys())[j]
      k = 0
      while k < len(self.adjacencyList[u]):
        v, weight = self.adjacencyList[u][k]
        # If negative-weight cycle detected, return None and negative infinity
        if distances[u] + weight < distances[v]:
          return None, float('-inf')
        k = k + 1
      j = j + 1

    # Reconstruct path
    path = []
    u = end
    while u is not None:
      # Insert airport at beginning of path list
      path.insert(0, u)
      u = predecessors[u]

    # Return shortest path and distance
    return path, distances[end]
