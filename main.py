from copy import deepcopy
from loader import Loader
from tsp import TSP

def main():
    path1 = "instancje/berlin11_modified.tsp"
    path2 = "instancje/kroA100.tsp"
    loader = Loader(path1)
    distance = loader.distance
    print(distance.matrix)
    population_size = 100
    generations = 100
    tour_size = 5
    px = 0.7
    pm = 0.1
    tsp = TSP(matrix = distance.matrix, population_size=population_size)
    cost, best = tsp.alg_loop(iterations=generations, tour_size=tour_size, px=px, pm=pm)
    print("cost:", cost, "best: ", best)

if __name__ == "__main__":
    main()
