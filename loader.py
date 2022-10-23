from models import City, Distance
import numpy as np

class Loader:
    def __init__(self, path: str):
        self.distance = self.process_input(path)

    def load_file(self, path: str):
        with open(path) as f:
            lines = f.readlines()
        return lines

    def process_input(self, path:str):
        lines = self.load_file(path)[6:-2]
        cities = []
        for count, line in enumerate(lines):
            try:
                city_id, x, y = line.split(" ")
                cities.append(City(int(float(city_id)), int(float(x)), int(float(y))))
            except ValueError:
                if count != 0:
                    print(line)
                    line = ' '.join(line.split())
                    try:
                        city_id, x, y, _ = line.split(" ")
                    except ValueError:
                        city_id, x, y = line.split(" ")
                    cities.append(City(int(float(city_id)), int(float(x)), int(float(y))))
                            
            
        matrix = np.empty((len(cities), len(cities)), dtype=int)

        for i in range(len(cities)):
            for j in range(len(cities)):
                matrix[i][j] = self.count_distance(cities[i].x, cities[j].x, cities[i].y, cities[j].y)

        distance = Distance(matrix)
        return distance
    
    def count_distance(self, x1, x2, y1, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5