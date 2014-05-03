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
INDEX_OUT = "index.html"
JS_OUT = "../natural-neighbourhood-pages/heatmap-data"


class Neighourhoods:
    """
    Class for building natural neighbourhood heatmap.
    """

    def __init__(self, data_source):                
        """
        Constructor: requires a CSV file as argument.
        """
        
        self.data = []
        self.nn_dict = {}
        self.nn_names = []
        self.fromCSV(data_source)
        self.nn_coords()
        
        
    def fromCSV(self, data_source, verbose=True):
        """
        Read in coordinate data from a CSV file
        """
        reader = csv.reader(open(data_source, "rU"))
        if verbose:
            print("Reading in the file '%s'\n" % data_source)
        next(reader)
        self.data = reader
        
            
    def nn_coords(self, verbose=True):
        """
        Build a dictionary that maps neighbourhood names into a list of
        coordinates, one for each survey response.
        """
        
        d = defaultdict(list)
        for line in self.data:
            geo = tuple(line[4:6])
            nn_name = self.standardise(line[2])
            d[nn_name].append(geo)        
        self.nn_dict = d
        self.nn_names = sorted(self.nn_dict.keys())
        if verbose:
            print("Building dictionary with %s keys\n" % len(d))        
        
        
    def standardise(self, name):
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
            #nn = self.uglify(nn)
            fn = os.path.join(subdir, nn + '.js')
            header = ("var %s = \n" % nn)
            contents = header + json.dumps(vals)
            with open(fn, "w") as outfile:
                outfile.write(contents)
                print("[%s] Writing to %s" % (count,fn))
            count = count + 1
            
    def js_headers(self):
        
        header_tmpl = '<script src="%s.js" type="text/javascript"></script>'
        headers = [(header_tmpl % nn) for nn in self.nn_names]
        headers = "\n".join(headers)
        return headers
        
            
        
    
def main():   
    nns = Neighourhoods(CSV_IN)
    nns.dump_address_points(JS_OUT)
    headers = nns.js_headers()
    pass
    
    
        
if __name__ == "__main__":
            main() 