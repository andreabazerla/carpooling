import utm
import converter

class Point:
    def __init__(self, origin=None, polar_coordinate=None, cartesian_coordinate=None, geographic_coordinate=None):
        self.origin = origin
        self.polar_coordinate = polar_coordinate
        self.cartesian_coordinate = cartesian_coordinate
        self.geographic_coordinate = geographic_coordinate

        self.build_coordinate()

    def get_polar_coordinate(self):
        return self.polar_coordinate

    def get_cartesian_coordinate(self):
        return self.cartesian_coordinate
    
    def get_geographic_coordinate(self):
        return self.geographic_coordinate

    def polar_2_cartesian(self):
        self.cartesian_coordinate = converter.polar_2_cartesian(self.polar_coordinate)
    
    def cartesian_2_polar(self):
        self.polar_coordinate = converter.cartesian_2_polar(self.cartesian_coordinate)

    def cartesian_2_geographic(self):
        if self.origin is not None:
            origin = self.get_translation(self.origin)
            cartesian_point = (self.cartesian_coordinate[0] + origin[0], self.cartesian_coordinate[1] + origin[1])
        else:
            cartesian_point = (self.cartesian_coordinate[0], self.cartesian_coordinate[1])
        
        self.geographic_coordinate = utm.to_latlon(cartesian_point[0], cartesian_point[1], 32, 'T')

    def get_translation(self, origin):
        origin_translated = utm.from_latlon(origin[0], origin[1])
        return (origin_translated[0], origin_translated[1])

    def build_coordinate(self):
        if self.polar_coordinate is None:
            if self.geographic_coordinate is not None:
                self.cartesian_2_polar()
                self.geographic_2_cartesian()
        elif self.polar_coordinate is not None:
            if self.geographic_coordinate is None:
                self.polar_2_cartesian()
                self.cartesian_2_geographic()

    def __str__(self):
        point_string = '['

        coordinate_string = []
        if self.polar_coordinate is not None:
            coordinate_string.append(str(self.polar_coordinate))
        
        if self.cartesian_coordinate is not None:
            coordinate_string.append(str(self.cartesian_coordinate))

        if self.geographic_coordinate is not None:
            coordinate_string.append(str(self.geographic_coordinate))
        
        point_string += ', '.join(coordinate_string)

        point_string += ']'

        return point_string