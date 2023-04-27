import random
import string

abbreviations = set()

while len(abbreviations) < 1000:
    abbreviation = ''.join(random.choices(string.ascii_uppercase, k=3))
    abbreviations.add(abbreviation)
airports = list(abbreviations)


min_distance = 125 # minimum distance in miles
max_distance = 1000 # maximum distance in miles
num_routes = 100000 # number of routes to generate

routes = set()

while len(routes) < num_routes:
    route = (random.choice(airports), random.choice(airports))
    if route[0] != route[1]: # ensure that the route does not start and end at the same airport
        distance = random.randint(min_distance, max_distance)
        route_str = route[0] + ',' + route[1] + ',' + str(distance)
        routes.add(route_str)

with open('testRoutes1.txt', 'w') as f:
    for route in routes:
        f.write(route + '\n')