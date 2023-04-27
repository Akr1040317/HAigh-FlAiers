from route import Route
from airportGraph import AirportGraph
import re
import time

def main():
  routeGraph = AirportGraph()
  # read in the routes from the file
  with open("testRoutes1.txt", mode="r") as file:
    for line in file:
      if len(line) >= 11:
        route = Route(line[0:3], line[4:7], int(line[8:11]))
        routeGraph.addRoute(route)

#begin welcoming the user, basic UI
  print("Welcome to the airport route optimization program!")
  print("-----------------------------------")
  print("The program will take in a starting airport and ending airport")
  print("and will print out the sequence of 1-leg flights to take to ")
  print("satisfy that route!")
  print("------------------------------------")
  print()

  flag = True
  
  while (flag):
    # accept inputs
    start = input("Enter the starting airport: ")
    end = input("Enter the ending airport: ")
    print()
    # validate inputs
    while ((not re.search("^[A-Z]{3}$", start)) and
           (not re.search("^[A-Z]{3}$", end))
           or not (start in routeGraph.adjacencyList.keys())
           or not (end in routeGraph.adjacencyList.keys()) or start == end):
      print(
        "Please input existing airports in the right format (2 different strings of 3 capital letters)."
      )
      start = input("Enter the starting airport: ")
      end = input("Enter the ending airport: ")
      print()

    # run Dijkstra's 
    print("Dijkstra's")
    print("-----------")
    # time execution
    start_time = time.time()
    path, distance = routeGraph.find_shortest_path_dijkstra(start, end)
    end_time = time.time()
    if (path == None):
      print("A route does not exist between the two airports provided")
    else:
      print("The shortest path is", "->".join(path))
      print("The distance is", distance)
      print(f"Dijkstra's algorithm took {end_time - start_time:.6f} seconds to run.")
    print()

    # run Bellman Ford
    print("Bellman Ford")
    print("-----------")
    # time execution
    start_time = time.time()
    path, distance = routeGraph.find_shortest_path_bellman_ford(start, end)
    end_time = time.time()
    if path is None:
      print("A route does not exist between the two airports provided")
    else:
      print("The shortest path is", "->".join(path))
      print("The distance is", distance)
      print(f"Bellman Ford algorithm took {end_time - start_time:.6f} seconds to run.")
    print()
    # run ML
    print("Machine Learning Model")
    print("----------------------")
    print("Coming soon.")
    print()
    
    # ask if user wants to continue
    continueResponse = input("Do you have more routes to optimize? (Y/N) ")
    while (not re.search("^[YN]$", continueResponse)):
      continueResponse = input("Please input either Y or N: ")

    if (continueResponse == "N"):
      flag = False

    print()

  print("Thanks for using the program!")


if (__name__ == "__main__"):
  main()
