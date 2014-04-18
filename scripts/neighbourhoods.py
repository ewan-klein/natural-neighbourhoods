"""

"""

from collections import Counter, defaultdict, namedtuple
import csv
import json
import os


CSV_IN = "../nn_data_normalised.csv"


class Neighourhoods(object):
    """"""

    def __init__(self, data_source):                
        """
        Constructor
        """
        
        self.data = []
        self.nn_dict = {}
        
        
    def read(self, data_source):
        """
        Read data in from a CSV file
        """
        reader = csv.reader(open(data_source, "rU"))
        next(reader)
        self.data = reader
            
    def nn_coords(self):
        """
        Build a dictionary that maps neighbourhood names into a list of
        coordinates, one for each survey response.
        """
        Coordinates = namedtuple('Coordinates', 'postcode, lat, lng')
        d = defaultdict(list)
        for line in self.data:
            coords = Coordinates(line[3], line[4], line[5])
            nn_name = line[2]
            d[nn_name].append(coords)        
        self.nn_dict = d
        
    def dump_address_points(self, subdir, verbose=True):
        """
        Write a file of coordinates for each neighbourhood.
        """
        for nn in self.nn_dict:
            vals = self.nn_dict[nn]
            vals = [[float(coord.lat), float(coord.lng)] for coord in vals]
            fn = os.path.join(subdir, nn + '.js')
            header = "var addressPoints = \n"
            contents = header + json.dumps(vals)
            with open(fn, "w") as outfile:
                outfile.write(contents)
                print("Writing to %s" % fn)
    
def main():   
    nns = Neighourhoods(CSV_IN)
    nns.read(CSV_IN)
    nns.nn_coords()
    nns.dump_address_points('../heatmap_data')
    
    
        
if __name__ == "__main__":
            main() 