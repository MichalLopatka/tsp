from copy import deepcopy
from loader import Loader
from tsp import TSP, Random, Greedy
from time import perf_counter


def main():
    small1 = "instancje/berlin11_modified.tsp"
    small2 = "instancje/berlin52.tsp"
    medium1 = "instancje/kroA100.tsp"
    medium2 = "instancje/kroA150.tsp"
    medium3 = "instancje/kroA200.tsp"
    hard1 = "instancje/fl417.tsp"
    hard2 = "instancje/ali535.tsp"
    loader = Loader(hard2)
    distance = loader.distance
    print(distance.matrix)
    # population_size = 100
    # generations = 200
    # tour_size = 5
    # px = 0.7
    # pm = 0.3
    # for i in range(5, 6, 5):
    #     tour_size = i
    #     t1_start = perf_counter() 
    #     tsp = TSP(matrix = distance.matrix, population_size=population_size)
    #     cost, best = tsp.alg_loop(iterations=generations, tour_size=tour_size, px=px, pm=pm)
    #     print("cost:", cost, "best: ", best)
    #     t1_stop = perf_counter()
    #     print("Elapsed time:", t1_stop-t1_start)

    # random = Random(distance.matrix)
    # best, cost = random.find(10000)
    # print("cost:", cost, "best: ", best)

    greedy = Greedy(distance.matrix)
    best, cost = greedy.find()
    print("cost:", cost, "best: ", best)
if __name__ == "__main__":
    main()
