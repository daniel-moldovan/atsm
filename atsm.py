# Asymmetric travel sales man problem implementation
# v1.0.0

from utils import TextData
from itertools import permutations


class City:
    name = None
    distances = {}
    start_city = False

    def __init__(self, name, distances, start_city=False):
        self.name = name
        self.distances = distances
        self.start_city = start_city

    def distance_to(self, destination_name):
        return self.distances[destination_name]

    def get_closest_city(self, visited):
        best_distance = float('inf')
        closest_city = None
        for city, distance in self.distances.items():
            if distance < best_distance and distance != 0.0 and city not in visited:
                best_distance = distance
                closest_city = city

        return closest_city, best_distance

    def __repr__(self):
        return '<{}>'.format(self.name)


class Tour:
    _cities = []
    _tours = []

    def __init__(self):
        self._cities = []
        self._tours = []

    def get_cities(self):
        return self._cities

    def add_city(self, city):
        self._cities.append(city)

    def get_city_by_name(self, name):
        for city in self._cities:
            if city.name == name:
                return city
        return None

    def get_start_city(self):
        for city in self._cities:
            if city.start_city:
                return city
        return None

    def set_start_city(self, name):
        for city in self._cities:
            city.start_city = False
            if city.name == name:
                city.start_city = True
        return None

    def get_path_steps(self, path):
        """
        Get steps of a specific path; Useful for calculating distance

        :param path eg: (<London>, <Edinburgh>, <Liverpool>, <Plymouth>, <Birmingham>, <London>):
        :return:
        eg: [(<London>, <Edinburgh>), (<Edinburgh>, <Liverpool>), (<Liverpool>, <Plymouth>),
         (<Plymouth>, <Birmingham>), (<Birmingham>, <London>)]
        """
        steps = []
        for i in range(len(path) - 1):
            steps.append((path[i], path[i + 1]))
        return steps

    def get_path_distance(self, path):
        """
        Get distance between cities in path(tour)

        :param path tuple of city objects:
        :return float:
        """
        distance = 0.0
        steps = self.get_path_steps(path)
        for origin_city, destination_city in steps:
            distance += origin_city.distance_to(destination_city.name)
        return distance

    def find_tour(self, debug=False):
        """
        Regular/naive method (sometimes called brute force method as well)
        Based on cities list it calculate tour distance for all possible combinations
        With this method we should identify always the best tour for the sales man

        :param debug bool:
        :return: min distance and correspondent path
        """
        start_city = self.get_start_city()
        all_tours = permutations(self._cities)
        for tour in all_tours:
            if tour[0].name == start_city.name:
                self._tours.append(tour + (start_city,))

        best_tour = min(self._tours, key=lambda p: self.get_path_distance(p))

        if debug:
            for tour in self._tours:
                print("Tour", tour, self.get_path_distance(tour))
            print(len(self._tours))

        # beatify result
        best_tour_path = ''
        for city in best_tour:
            best_tour_path += city.name + ' -> '
        best_tour_path = best_tour_path[0:len(best_tour_path) - 4]
        return best_tour_path, round(self.get_path_distance(best_tour), 2)

    def find_tour_greedy(self, debug=False):
        """
        This is a faster method to get the best tour for the sales man
        This algorithm on average will give us a tour 25% longer than the shortest possible one.

        :param debug bool:
        :return min distance and correspondent path:
        """
        path = []
        visited = []
        next_city = self.get_start_city()
        visited.append(next_city.name)
        path.append(next_city)
        while len(path) < len(self._cities):
            next_city, dist = next_city.get_closest_city(visited)
            next_city = self.get_city_by_name(next_city)
            visited.append(next_city.name)
            path.append(next_city)
            if debug:
                print("Next city", next_city)
        path.append(self.get_start_city())
        best_tour = tuple(path)

        # beatify result
        best_tour_path = ''
        for city in best_tour:
            best_tour_path += city.name + ' -> '
        best_tour_path = best_tour_path[0:len(best_tour_path) - 4]
        return best_tour_path, round(self.get_path_distance(best_tour), 2)


if __name__ == "__main__":
    # tested with Python 3.6
    # Use case 1
    # Read city & distances from file
    print(' # Use case 1 - brute force method')
    tour = Tour()
    data = TextData("cities_and_distances.txt")
    for city in data.cities:
        tour.add_city(City(name=city, distances=data.distances[city]))
    tour.set_start_city('London')
    print(tour.find_tour())
    tour.set_start_city('Edinburgh')
    print(tour.find_tour())
    # example of output:
    # ('London -> Birmingham -> Liverpool -> Edinburgh -> Plymouth -> London', 26.910000000000004)
    # ('Edinburgh -> Plymouth -> London -> Birmingham -> Liverpool -> Edinburgh', 26.91)

    # Use case 2
    # Use greedy algorithm
    print("\n")
    print(' # Use case 2 - greedy method')
    tour = Tour()
    data = TextData("cities_and_distances.txt")
    for city in data.cities:
        tour.add_city(City(name=city, distances=data.distances[city]))
    tour.set_start_city('London')
    print(tour.find_tour_greedy())
    tour.set_start_city('Edinburgh')
    print(tour.find_tour_greedy())

    # example of output:
    # ('London -> Birmingham -> Liverpool -> Edinburgh -> Plymouth -> London', 26.91)
    # ('Edinburgh -> Liverpool -> Birmingham -> London -> Plymouth -> Edinburgh', 27.3)


    # Alternative use case
    # Add data manually in code
    # print("\n")
    # print(' # Use case 2 - read data from code')
    # tour = Tour()
    # city = City(name='London', distances={'London': 0.0, 'Edinburgh': 6.47, 'Liverpool': 7.1,
    #                                       'Plymouth': 6.1, 'Birmingham': 3.56})
    # tour.add_city(city)
    # city = City(name='Edinburgh', distances={'London': 7.14, 'Edinburgh': 0.0, 'Liverpool': 4.42,
    #                                          'Plymouth': 9.3, 'Birmingham': 7.39})
    # tour.add_city(city)
    # city = City(name='Liverpool', distances={'London': 7.0, 'Edinburgh': 4.48, 'Liverpool': 0.0,
    #                                          'Plymouth': 13.37, 'Birmingham': 3.14})
    # tour.add_city(city)
    # city = City(name='Plymouth', distances={'London': 6.24, 'Edinburgh': 9.34, 'Liverpool': 13.36,
    #                                         'Plymouth': 0.0, 'Birmingham': 10.12})
    # tour.add_city(city)
    # city = City(name='Birmingham', distances={'London': 4.3, 'Edinburgh': 7.45, 'Liverpool': 3.33,
    #                                           'Plymouth': 10.17, 'Birmingham': 0.0})
    # tour.add_city(city)
    # tour.set_start_city('London')
    # print(tour.find_tour())
    # tour.set_start_city('Edinburgh')
    # print(tour.find_tour())
