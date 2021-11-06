from math import dist
import random
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
from random import uniform
from Point import Point
import converter
import utm

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