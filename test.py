import os
from dotenv.main import load_dotenv
import networkx as nx
import matplotlib.pyplot as plt

from Generator import Generator
from Map import Map
from StudentType import StudentType

UNIFE_COORDINATES = (44.83436, 11.59934)

students_number = 1000
drivers_percentage = 12
mean = 1000
sd = 5000
low = 1000
upp = 10000

generator = Generator(UNIFE_COORDINATES, students_number, drivers_percentage, mean, sd, low, upp)

students_coordinates = generator.get_students_coordinates()

drivers_coordinates = generator.get_drivers_coordinates(students_coordinates)
print(drivers_coordinates)

passengers_coordinates = generator.get_passengers_coordinates(students_coordinates)
print(passengers_coordinates)

# generator.show_distances_distribution()
# generator.show_angles_distribution()
# generator.show_polar_coordinates()
# generator.show_cartesian_coordinates()

load_dotenv()

MAPS_JAVASCRIPT_API = os.getenv('MAPS_JAVASCRIPT_API')

gmap = Map(MAPS_JAVASCRIPT_API, 'map.html', UNIFE_COORDINATES, drivers_coordinates, passengers_coordinates)

gmap.build_map()
gmap.draw_map()
gmap.show_map()

idx = 0

drivers_nodes = []
for driver_coordinates in drivers_coordinates:
    drivers_nodes.append((idx, {'type': StudentType.DRIVER.value, 'latitude': driver_coordinates[0], 'longitude': driver_coordinates[1]}))
    idx = idx + 1
# print(len(drivers_nodes))

passengers_nodes = []
for passenger_coordinates in passengers_coordinates:
    passengers_nodes.append((idx, {'type': StudentType.PASSENGER.value, 'latitude': passenger_coordinates[0], 'longitude': passenger_coordinates[1]}))
    idx = idx + 1
# print(len(passengers_nodes))

G = nx.Graph()

students_nodes = [*drivers_nodes, *passengers_nodes]
# print(len(students_nodes))
# print(students_nodes)

G.add_nodes_from(students_nodes)

options = {
    'node_size': 50,
}

node_color = []
for student_node in G.nodes(data=True):
    if student_node[1]['type'] == 0:
        node_color.append('yellow')
    elif student_node[1]['type'] == 1:
        node_color.append('blue')

nx.draw(G, with_labels=True, node_color=node_color, **options)
plt.show()