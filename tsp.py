import numpy as np
import random
from copy import deepcopy

class TSP:
    def __init__(self, matrix: np.array, population_size: int):
        self.matrix = matrix
        self.length = matrix.shape[0]
        self.population_size = population_size
        self.population = self.create_population()

    def alg_loop(self, iterations: int, tour_size: int, px: float, pm: float) -> tuple[int, list[int]]:
        t = 0
        population = self.population
        while (t < iterations):
            new_population = []
            while (len(new_population) < self.population_size):
                chosen1 = self.tournament(population, tour_size)
                # print("ch1:", chosen1)
                chosen2 = self.tournament(population, tour_size)
                # print("ch2:", chosen2)
                if (random.random() < px):
                    crossed = self.ox(chosen1, chosen2)
                else:
                    crossed = chosen1
                # print("cro:", crossed)
                if (random.random() < pm):
                    mutated = self.swap(crossed)
                    new_population.append(mutated)
                else:
                    new_population.append(crossed)
            t+=1
            population = new_population
        best = self.tournament(population, len(population))
        return self.cost(self.matrix, best), best

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

    def cost(self, cost_mat, route):
        return cost_mat[np.roll(route, 1), route].sum()

    def swap(self, order: list[int]):
        pos1, pos2 = random.sample(order, 2)
        order[pos1], order[pos2] = order[pos2], order[pos1]
        return order

    def inverse(self, order: list[int]):
        pos1, pos2 = random.sample(order, 2)
        if pos2 > pos1:
            order[pos1:pos2] = order[pos2-1:pos1-1:-1]
        elif pos1 > pos2:
            order[pos2:pos1] = order[pos1-1:pos2-1:-1]
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

    def pmx(self, order1: list[int], order2: list[int]) -> tuple[list[int], list[int]]:
        left = random.randint(0, len(order1) - 1)
        right = random.randint(left + 1, len(order1))
        subsection1 = order1[left:right]
        subsection2 = order2[left:right]
        mapping1 = {}
        mapping2 = {}
        for i in range(len(subsection1)):
            mapping1[subsection1[i]] = subsection2[i]
            mapping2[subsection2[i]] = subsection1[i]
        return_order1 = deepcopy(order1)
        return_order2 = deepcopy(order2)
        for i in range(len(return_order1)):
            if return_order1[i] in subsection1:
                return_order1[i] = mapping1[return_order1[i]]
            elif return_order1[i] in mapping2:
                return_order1[i] = mapping2[return_order1[i]]
        for i in range(len(return_order2)):
            if return_order2[i] in subsection2:
                return_order2[i] = mapping2[return_order2[i]]
            elif return_order2[i] in mapping1:
                return_order2[i] = mapping1[return_order2[i]]
        return return_order1, return_order2

    def tournament(self, population: list[list[int]], sample_size: int) -> list[int]:
        sample = random.sample(population, sample_size)
        best = None
        for el in sample:
            if not best or self.cost(self.matrix, el) < self.cost(self.matrix, best):
                best = el
        return best