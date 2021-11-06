import gmplot
import webbrowser, os

class Map:
    def __init__(self, apikey, filename, origin, upp, drivers_coordinates, passengers_coordinates, zoom=12):
        self.apikey = apikey
        self.filename = filename
        self.origin = origin
        self.upp = upp
        self.gmap = gmplot.GoogleMapPlotter(origin[0], origin[1], zoom, apikey=self.apikey)
        self.drivers_coordinates = drivers_coordinates
        self.passengers_coordinates = passengers_coordinates
    
    def build_map(self):
        self.add_marker(marker=self.origin, color='#ff0000')

        labels = [str(x) for x in list(range(len(self.drivers_coordinates) + len(self.passengers_coordinates)))]
        
        drivers_coordinates = []
        for i in self.drivers_coordinates:
            drivers_coordinates.append(i.get_geographic_coordinate())
        
        passengers_coordinates = []
        for i in self.passengers_coordinates:
            passengers_coordinates.append(i.get_geographic_coordinate())

        self.add_points(points=drivers_coordinates, color='#ffff00', labels=labels[:len(drivers_coordinates)])
        self.add_points(points=passengers_coordinates, color='#0000ff', labels=labels[len(drivers_coordinates):])
        self.add_circle(self.origin, self.upp)

    def show_map(self):
        self.open_map()

    def add_marker(self, marker, color):
        self.gmap.marker(marker[0], marker[1], color=color)

    def add_points(self, points, color, size=1, marker=True, labels=[]):
        points_lat, points_lon = zip(*points)
        self.gmap.scatter(points_lat, points_lon, color=color, size=size, marker=marker, label=labels)

    def add_circle(self, origin, radius):
        self.gmap.circle(origin[0], origin[1], radius, face_alpha=0, edge_color='#000000', edge_width=3)

    def draw_map(self):
        self.gmap.draw(self.filename)

    def open_map(self):
        webbrowser.open('file://' + os.path.realpath(self.filename))