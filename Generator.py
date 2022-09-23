from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import networkx as nx
from random import uniform
from dotenv.main import load_dotenv
from haversine import haversine, Unit
import os
import math

from Point import Point
from NodeType import NodeType
from NodeStatus import NodeStatus
from Map import Map
class Generator:
    polar_coordinates = []
    cartesian_coordinates = []
    geographic_coordinates = []
    origin_node = None
    G = None

    def __init__(self, origin, students_number, drivers_percentage, mean, sd, low, upp):
        self.origin = origin
        self.students_number = students_number
        self.drivers_percentage = drivers_percentage
        self.mean = mean
        self.sd = sd
        self.low = low
        self.upp = upp

    def get_origin_node(self):
        return self.origin_node

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

    def get_origin_coordinates(self):
        return Point(origin=self.origin, polar_coordinate=(0, 0))

    def get_drivers_number(self):
        return int(self.drivers_percentage * self.students_number / 100)
    
    def get_drivers_coordinates(self, students_coordinates):
        drivers_number = self.get_drivers_number()
        return students_coordinates[:drivers_number]

    def get_passengers_coordinates(self, students_coordinates):
        drivers_number = self.get_drivers_number()
        return students_coordinates[drivers_number:]

    def driver_exists(self, graph):
        for i in graph:
            if i[1]['t'] == NodeType.DRIVER.value:
                return True
    
    def get_distance_cartesian(self, i, j):
        return math.sqrt((i[1]['c'][0]-j[1]['c'][0])**2+(i[1]['c'][1]-j[1]['c'][1])**2)

    def get_distance_geographic(self, i, j):
        return round(haversine(i[1]['g'], j[1]['g'], unit=Unit.METERS))

    def set_edge(self, i, j, graph):
        if (i[0] != j[0]):
            if j[1]['t'] == NodeType.ORIGIN.value:
                return True
        return False

    def build_graph(self, origin_coordinates, drivers_coordinates, passengers_coordinates):
        global origin_node
        
        idx = 0

        origin_node = (idx, {
            't': NodeType.ORIGIN.value,
            's': NodeStatus.FREE.value,
            'p': origin_coordinates.get_polar_coordinate(),
            'c': origin_coordinates.get_cartesian_coordinate(),
            'g': origin_coordinates.get_geographic_coordinate(),
        })
        self.origin_node = origin_node
        idx = idx + 1

        drivers_nodes = []
        for driver_coordinates in drivers_coordinates:
            drivers_nodes.append((idx, {
                't': NodeType.DRIVER.value,
                's': NodeStatus.FREE.value,
                'p': driver_coordinates.get_polar_coordinate(),
                'c': driver_coordinates.get_cartesian_coordinate(),
                'g': driver_coordinates.get_geographic_coordinate(),
            }))
            idx = idx + 1

        passengers_nodes = []
        for passenger_coordinates in passengers_coordinates:
            passengers_nodes.append((idx, {
                't': NodeType.PASSENGER.value,
                's': NodeStatus.FREE.value,
                'p': passenger_coordinates.get_polar_coordinate(),
                'c': passenger_coordinates.get_cartesian_coordinate(),
                'g': passenger_coordinates.get_geographic_coordinate(),    
            }))
            idx = idx + 1

        G = nx.Graph()

        nodes = [origin_node, *drivers_nodes, *passengers_nodes]

        G.add_nodes_from(nodes)

        passengers_edge_list = []
        for i in G.nodes(data=True):
            for j in G.nodes(data=True):
                if self.set_edge(i, j, G.nodes(data=True)):
                    passengers_edge_list.append((i[0], j[0], { 'distance': self.get_distance_geographic(i, j) }))

        G.add_edges_from(passengers_edge_list)

        self.G = G

        return G

    def get_total_distance(self, G):
        total_distance = 0
        
        for _, _, data in G.edges(data=True):
            total_distance = total_distance + data['distance']
        
        return total_distance

    def get_graph(self):
        return self.G

    @staticmethod
    def show_graph(G, update=False, pause=False, interval=0.1):
        pos = []
        node_color = []
        for node in G.nodes(data=True):

            pos.append(node[1]['c'])

            node_type = node[1]['t']
            if node_type == NodeType.ORIGIN.value:
                node_color.append('black')
            if node_type == NodeType.DRIVER.value:
                node_color.append('red')
            elif node_type == NodeType.PASSENGER.value:
                node_color.append('yellow')

        options = {
            'node_size': 50,
        }

        if update:
            plt.clf()
        
        nx.draw(G, with_labels=True, node_color=node_color, pos=pos, **options)
        
        if update and pause:
            plt.pause(interval)
        
        if not update:
            plt.show()
    
    def show_map(self, origin, upp, drivers_coordinates, passengers_coordinates):
        load_dotenv()

        MAPS_JAVASCRIPT_API = os.getenv('MAPS_JAVASCRIPT_API')

        gmap = Map(MAPS_JAVASCRIPT_API, 'map.html', origin, upp, drivers_coordinates, passengers_coordinates)

        gmap.build_map()
        gmap.draw_map()
        gmap.show_map()

    @staticmethod
    def read_graph(path):
        return nx.read_gml(path)

    def write_graph(self, G, path):
        return nx.write_gml(G, path)