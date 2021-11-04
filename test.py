import os
from dotenv.main import load_dotenv

from generator import Generator
from map import Map

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
passengers_coordinates = generator.get_passengers_coordinates(students_coordinates)

generator.show_distances_distribution()
generator.show_angles_distribution()
generator.show_polar_coordinates()
generator.show_cartesian_coordinates()

load_dotenv()

MAPS_JAVASCRIPT_API = os.getenv('MAPS_JAVASCRIPT_API')

gmap = Map(MAPS_JAVASCRIPT_API, 'map.html', UNIFE_COORDINATES, drivers_coordinates, passengers_coordinates)

gmap.build_map()
gmap.draw_map()
gmap.show_map()