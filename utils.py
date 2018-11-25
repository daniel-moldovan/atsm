class TextData():
    cities = []
    distances = {}

    def __init__(self, source_path):
        with open(source_path, 'r') as source:
            data = source.read()
            table = ([i.split() for i in data.split("\n")])[1:-1]
            cities = [line[0] for line in table]
            distance_table = {}
            for line in table:
                distance_table[line[0]] = {}
                for city, distance in zip(cities, line[1:]):
                    distance_table[line[0]][city] = float(distance)

        self.distances = distance_table
        self.cities = cities
