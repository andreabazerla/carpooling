import matplotlib.pyplot as plt
from scipy.stats import truncnorm
from random import uniform
from Point import Point
import networkx as nx
from Map import Map
from dotenv.main import load_dotenv
import os
from StudentType import StudentType
class Generator:
    polar_coordinates = []
    cartesian_coordinates = []
    geographic_coordinates = []

    def __init__(self, origin, students_number, drivers_percentage, mean, sd, low, upp):
        self.origin = origin
        self.students_number = students_number
        self.drivers_percentage = drivers_percentage
        self.mean = mean
        self.sd = sd
        self.low = low
        self.upp = upp

    def get_truncated_normal_distribution(self, mean=0, sd=1, low=0, upp=1000):
        return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

    def get_random_distance(self):
        distribution = self.get_truncated_normal_distribution(self.mean, self.sd, self.low, self.upp)
        distances = distribution.rvs(self.students_number)
        return distances

    def get_random_angles(self):
        angles = []
        for _ in range(self.students_number):
            angles.append(uniform(0, 360))
        return angles

    def coordinates_2_polar(self, distances, angles):
        polar_coordinates = list(zip(distances, angles))
        self.polar_coordinates = polar_coordinates
        return polar_coordinates

    def show_distribution_histogram(self, values, label_x, label_y):
        plt.figure()
        plt.hist(values)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.show()

    def get_polar_coordinates_unzipped(self):
        return list(zip(*self.polar_coordinates))

    def get_distances(self):
        polar_coordinates_unzipped = self.get_polar_coordinates_unzipped()
        return polar_coordinates_unzipped[0]

    def get_angles(self):
        polar_coordinates_unzipped = self.get_polar_coordinates_unzipped()
        return polar_coordinates_unzipped[1]

    def show_distances_distribution(self):
        distances = self.get_distances()
        self.show_distribution_histogram(distances, 'Meters from origin', 'Number of students')

    def show_angles_distribution(self):
        angles = self.get_angles()
        self.show_distribution_histogram(angles, 'Degree', 'Number of students')

    def show_polar_coordinates(self):
        polar_coordinates_unzipped = list(zip(*self.polar_coordinates))
        distances = polar_coordinates_unzipped[0]
        angles = polar_coordinates_unzipped[1]

        plt.figure()
        plt.polar(angles, distances, 'k.')
        plt.show()

    def show_cartesian_coordinates(self):
        cartesian_coordinates_unzipped = list(zip(*self.cartesian_coordinates))
        
        plt.figure()
        plt.scatter(cartesian_coordinates_unzipped[0], cartesian_coordinates_unzipped[1])
        plt.show()

    def get_students_coordinates(self):
        polar_coordinates = self.coordinates_2_polar(self.get_random_distance(), self.get_random_angles())

        students_coordinates = []
        for polar_point in polar_coordinates:
            students_coordinates.append(Point(origin=self.origin, polar_coordinate=polar_point))

        for i in students_coordinates:
            self.cartesian_coordinates.append(i.get_cartesian_coordinate())
            self.geographic_coordinates.append(i.get_geographic_coordinate())
        
        return students_coordinates

    def get_drivers_number(self):
        return int(self.drivers_percentage * self.students_number / 100)
    
    def get_drivers_coordinates(self, students_coordinates):
        drivers_number = self.get_drivers_number()
        return students_coordinates[:drivers_number]

    def get_passengers_coordinates(self, students_coordinates):
        drivers_number = self.get_drivers_number()
        return students_coordinates[drivers_number:]

    def show_graph(self, drivers_coordinates, passengers_coordinates):


        idx = 0

        drivers_nodes = []
        for driver_coordinates in drivers_coordinates:
            drivers_nodes.append((idx, {'type': StudentType.DRIVER.value,
                'polar_coordinate': driver_coordinates.get_polar_coordinate(),
                'cartesian_coordinate': driver_coordinates.get_cartesian_coordinate(),
                'geographic_coordinate': driver_coordinates.get_geographic_coordinate(),
            }))
            idx = idx + 1

        passengers_nodes = []
        for passenger_coordinates in passengers_coordinates:
            passengers_nodes.append((idx, {'type': StudentType.PASSENGER.value,
                'polar_coordinate': passenger_coordinates.get_polar_coordinate(),
                'cartesian_coordinate': passenger_coordinates.get_cartesian_coordinate(),
                'geographic_coordinate': passenger_coordinates.get_geographic_coordinate(),    
            }))
            idx = idx + 1

        G = nx.Graph()

        students_nodes = [*drivers_nodes, *passengers_nodes]

        G.add_nodes_from(students_nodes)

        pos = []
        for i in students_nodes:
            pos.append(i[1]['cartesian_coordinate'])

        node_color = []
        for student_node in G.nodes(data=True):
            if student_node[1]['type'] == 0:
                node_color.append('yellow')
            elif student_node[1]['type'] == 1:
                node_color.append('blue')

        options = {
            'node_size': 50,
        }

        nx.draw(G, with_labels=True, node_color=node_color, pos=pos, **options)
        plt.show()
    
    def show_map(self, origin, upp, drivers_coordinates, passengers_coordinates):
        load_dotenv()

        MAPS_JAVASCRIPT_API = os.getenv('MAPS_JAVASCRIPT_API')

        gmap = Map(MAPS_JAVASCRIPT_API, 'map.html', origin, upp, drivers_coordinates, passengers_coordinates)

        gmap.build_map()
        gmap.draw_map()
        gmap.show_map()