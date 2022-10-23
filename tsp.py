import numpy as np
import random
from copy import deepcopy
import numpy.random as npr
import math 


class TSP:
    def __init__(self, matrix: np.array, population_size: int):
        self.matrix = matrix
        self.length = matrix.shape[0]
        self.population_size = population_size
        self.population = self.create_population()

    def alg_loop(self, iterations: int, tour_size: int, px: float, pm: float) -> tuple[int, list[int]]:
        t = 0
        population = self.population
        f = open('test.csv', 'a')
        
        while (t < iterations):
            new_population = []
            while (len(new_population) < self.population_size):
                chosen1 = self.roulette(population)
                chosen2 = self.roulette(population)
                if (random.random() < px):
                    crossed1, crossed2 = self.pmx(chosen1, chosen2)
                    # print(crossed1, crossed2)
                else:
                    crossed1, crossed2 = chosen1, chosen2
                if (random.random() < pm):
                    mutated1 = self.inverse(crossed1)
                    mutated2 = self.inverse(crossed2)
                    # print(mutated)
                    new_population.append(mutated1)
                    new_population.append(mutated2)
                    
                else:
                    new_population.append(crossed1)
                    new_population.append(crossed2)
            t+=1
            population = new_population
            best = self.tournament(new_population, len(new_population))
            cost = self.cost(best)
            worst = self.worst(new_population)
            cost_worst = self.cost(worst)
            mean = self.mean(new_population)
            data = f"{t}; {cost};{cost_worst};{mean};;;\n"
            # print(data)
            f.writelines(data)
        best = self.tournament(new_population, len(new_population))
        f.close()
        return self.cost(best), best

    def create_population(self) -> list[int]:
        population = []
        for i in range(self.population_size):
            begin = self.random_start(self.length)
            population.append(begin)
        return population

    def random_start(self, len) -> list[int]:
        begin = list(range(0, len))
        random.shuffle(begin)
        return begin

    def cost(self, route):
        return self.matrix[np.roll(route, 1), route].sum()

    def swap(self, order: list[int]):
        pos1, pos2 = random.sample(order, 2)
        order[pos1], order[pos2] = order[pos2], order[pos1]
        return order

    def inverse(self, order: list[int]):
        pos1 = random.randint(0, len(order) - 1)
        pos2 = random.randint(pos1 + 1, len(order))
        order[pos1:pos2] = order[pos1:pos2][::-1]
        return order

    def ox(self, order1: list[int], order2: list[int]) -> list[int]:
        left = random.randint(0, len(order1) - 1)
        right = random.randint(left + 1, len(order1))
        part1 = order1[left:right]
        new_order  = [None] * len(order2)
        new_order[left:right] = part1
        order2 = [x for x in order2 if x not in part1]
        j = 0
        return_order = []
        for i in range(len(new_order)):
            if new_order[i] is None:
                return_order.append(order2[j])
                j += 1 
            else:
                return_order.append(new_order[i])
        return return_order


    def pmx_looking(
        self, mapping_primary, mapping_secondary, value: int
    ) -> int:
        while value in mapping_primary:
            value = mapping_secondary[mapping_primary.index(value)]
        return value

    def pmx(self, order1: list[int], order2: list[int]) -> tuple[list[int], list[int]]:
        left = random.randint(0, len(order1) - 1)
        right = random.randint(left + 1, len(order1))
        return_order1 = [-1]*len(order1)
        return_order2 = [-1]*len(order2)
        mapping1 = order1[left:right+1]
        mapping2 = order2[left:right+1]
        return_order1[left:right+1] = order2[left:right+1]
        return_order2[left:right+1] = order1[left:right+1]
        for i in range(len(order1)):
            if i >= left and i <= right:
                continue
            if order1[i] in mapping2:
                return_order1[i] = self.pmx_looking(
                    mapping2, mapping1, order1[i]
                )
            else:
                return_order1[i] = order1[i]
        for i in range(len(order2)):
            if i >= left and i <= right:
                continue
            if order2[i] in mapping1:
                return_order2[i] = self.pmx_looking(
                    mapping1, mapping2, order2[i]
                )
            else:
                return_order2[i] = order2[i]
        # print(return_order1, return_order2)
        # print(" ")
        return return_order1, return_order2

    def tournament(self, population: list[list[int]], sample_size: int) -> list[int]:
        sample = random.sample(population, sample_size)
        best = None
        for el in sample:
            if not best or self.cost(el) < self.cost(best):
                best = el
        return best

    def roulette(self, population: list[list[int]]) -> list[int]:
        costs = [self.cost(pop) for pop in population]
        worst = self.cost(self.worst(population))
        diff = [(worst-c) for c in costs]
        # print(logs)
        max = sum([c for c in diff])
        # print(max)
        selection_probs = [c/max for c in diff]
        to_return = population[npr.choice(len(population), p=selection_probs)]
        # print(selection_probs)
        # print(to_return)
        return to_return 

    def worst(self, population: list[list[int]]) -> list[int]:
        worst = None
        for el in population:
            if not worst or self.cost(el) > self.cost(worst):
                worst = el
        return worst

    def mean(self, population: list[list[int]]) -> list[int]:
        sum = -1
        for el in population:
            sum += self.cost(el)
        mean = sum/len(population)
        return int(mean)


class Greedy:
    def __init__(
        self, matrix: np.array
    ):
        self.matrix = matrix
        self.matrix[self.matrix == 0] = 1000000
        self.length = matrix.shape[0]
        print(self.matrix)

    def modify_matrix(self, matrix: np.ndarray, current_city: int):
        matrix[current_city, :] = 1000000
        matrix[:, current_city] = 1000000
        return matrix

    def cost(self, route):
        return self.matrix[np.roll(route, 1), route].sum()

    def find(self):
        for start_city in range(self.length):
            best_route = []
            best_cost = -1
            matrix = np.copy(self.matrix)
            current_city = start_city
            route = []
            for idx in range(self.length):
                if idx == self.length -1:
                    continue
                next_city = matrix[current_city, :].argmin()
                matrix = self.modify_matrix(matrix, current_city)
                route.append(current_city)
                current_city = next_city
            if len(best_route) == 0 or self.cost(route) < best_cost:
                best_route = route
                best_cost = self.cost(route)
            return best_route, best_cost


class Random:
    def __init__(self, matrix: np.array):
        self.matrix = matrix
        self.length = matrix.shape[0]

    def cost(self, route):
        return self.matrix[np.roll(route, 1), route].sum()

    def random_start(self, len) -> list[int]:
        begin = list(range(0, len))
        random.shuffle(begin)
        return begin

    def find(self, n: int):
        best = []
        best_cost = -1
        for i in range(n):
            new = self.random_start(self.length)
            if len(best) == 0 or self.cost(new) < best_cost:
                best = new
                best_cost = self.cost(new)
        return best, best_cost

