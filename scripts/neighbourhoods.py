#!/usr/bin/env python
# Encoding: utf-8
# ----------------------------------------------------------------------------- 
# Author: Ewan Klein <ewan@raw-text.io>
# -----------------------------------------------------------------------------
# For license information, see LICENSE.txt
# -----------------------------------------------------------------------------
# 
# Script to convert 'natural neigbourhoods' CSV file into a heatmap
#

from collections import Counter, defaultdict
import csv
import json
import os
import shutil


CSV_IN = "../nn_data_normalised.csv"
HTMLDIR = "../natural-neighbourhood-pages"
INDEX-OUT = "index.html"
JS-OUT = "../natural-neighbourhood-pages/heatmap-data"


class Neighourhoods(object):
    """
    Class for building natural neighbourhood heatmap.
    """

    def __init__(self, data_source):                
        """
        Constructor: requires a CSV file as argument.
        """
        
        self.data = []
        self.nn_dict = {}
        
        
    def fromCSV(self, data_source):
        """
        Read in coordinate data from a CSV file
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
        """
        Convert a natural neighbourhood name into a standard format for
        filenames
        """
        name = name.lower()
        name = name.replace(" ", "_")
        name = name.replace("'", "")
        return name
        
    
    def dump_address_points(self, subdir, verbose=True):
        """
        Write a separate file of coordinates for each neighbourhood.
        
        The heatmap is built with a separate layer for each neighbourhood, so
        we need to create a separate file and an associated Javascript
        variable that is bound to the array of geographical coordinates.
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
    nns.fromCSV(CSV_IN)
    nns.nn_coords()
    nns.dump_address_points('../heatmap_data')
    
    
        
if __name__ == "__main__":
            main() 