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
from string import Template


CSV_IN = "../nn_data_normalised.csv"
HTMLDIR = "../natural-neighbourhoods-pages"
INDEX_OUT = "../../natural-neighbourhoods-pages/index.html"
JS_OUT = "../../natural-neighbourhoods-pages/heatmap-data"

HTML = """\
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head>
<title>Edinburgh Natural Neighbourhoods</title>
$leaflet
    <style>
     #map {
       width: 1024px;
       height: 768px; }
    </style>
</head>
<body>
    <div id="map"></div>
</body>
</html>
"""

LEAFLET = """\
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" />
<script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script>
<script src="leaflet-heat.js"></script>

$js_headers

<script>
 window.onload = function () {
    var map = L.map('map').setView([55.9436,-3.2100], 12);

    var tiles = L.tileLayer('http://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
     attribution: '<a href="https://www.mapbox.com/about/maps/">Terms and Feedback</a>',
     id: 'examples.map-20v6611k'
    }).addTo(map);
   
$js_layers
   
}
</script>
"""



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
        """
        Create a string representation of all the JS headers required.
        """        
        header_tmpl = '<script src="heatmap-data/%s.js" type="text/javascript"></script>'
        headers = [(header_tmpl % nn) for nn in self.nn_names]
        headers = "\n".join(headers)
        return headers
    
    def js_layers(self):
        layer_tmpl = """    var heatLayer%s = L.heatLayer(%s).addTo(map);"""
        layers = [(layer_tmpl % (nn.capitalize(),nn))for nn in self.nn_names]
        layers = "\n".join(layers)
        return layers
    
    
    def build_html(self, myoutfile):
        html = Template(HTML)
        leaflet = Template(LEAFLET)
        
        leaflet_str = leaflet.substitute(js_headers=self.js_headers(), js_layers=self.js_layers())
        
        output = html.substitute(leaflet=leaflet_str)
        
       
        with open(myoutfile, "w") as outfile:
            outfile.write(output)
            print("Writing to %s" % myoutfile)      
        
            
        
    
def main():   
    nns = Neighourhoods(CSV_IN)
    nns.dump_address_points(JS_OUT)
    nns.build_html(INDEX_OUT)

    
    
        
if __name__ == "__main__":
            main() 