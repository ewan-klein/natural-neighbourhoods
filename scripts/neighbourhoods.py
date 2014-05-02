"""

"""

from collections import Counter, defaultdict
import csv
import json
import os
import shutil


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
        d = defaultdict(list)
        for line in self.data:
            geo = tuple(line[4:6])
            nn_name = line[2]
            d[nn_name].append(geo)        
        self.nn_dict = d
        
    def uglify(self, name):
        name = name.lower()
        name = name.replace(" ", "_")
        name = name.replace("'", "")
        return name
        
    
    def dump_address_points(self, subdir, verbose=True):
        """
        Write a file of coordinates for each neighbourhood.
        """
        if os.path.exists(subdir):            
            shutil.rmtree(subdir)
        os.makedirs(subdir)
        count = 0
        
        for nn in self.nn_dict:
            vals = self.nn_dict[nn]
            vals = [[float(lat), float(lng)] for (lat, lng) in vals]
            nn = self.uglify(nn)
            fn = os.path.join(subdir, nn + '.js')
            header = ("var %s = \n" % nn)
            contents = header + json.dumps(vals)
            with open(fn, "w") as outfile:
                outfile.write(contents)
                print("[%s] Writing to %s" % (count,fn))
            count = count + 1
    
def main():   
    nns = Neighourhoods(CSV_IN)
    nns.read(CSV_IN)
    nns.nn_coords()
    nns.dump_address_points('../heatmap_data')
    
    
        
if __name__ == "__main__":
            main() 