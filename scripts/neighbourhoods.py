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
from colour import Color
import csv
from itertools import zip_longest
import json
import os
import shutil
from string import Template

import numpy as np




CSV_IN = "../nn_data_normalised.csv"
HTMLDIR = "../natural-neighbourhoods-pages"
INDEX_OUT = "../../natural-neighbourhoods-pages/index.html"
JS_OUT = "../../natural-neighbourhoods-pages/heatmap-data"
COLOURS = "nn_colours.csv"

HTML = """\
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head>
<title>Edinburgh Natural Neighbourhoods</title>
$leaflet
    <style>
     #map {
       width: 1200px;
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
    var map = L.map('map').setView([55.9436,-3.2100], 13);

    var tiles = L.tileLayer('http://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
     attribution: '<a href="https://www.mapbox.com/about/maps/">Terms and Feedback</a>',
     id: 'examples.map-20v6611k'
    }).addTo(map);
   
$js_layers
   
}
</script>
"""

class Neighbourhood(object):
    def __init__(self, name):                
            """
            Constructor: requires a CSV file as argument.
            """
            
            self.name = name
            self.colour = None
            self.centroid = None
            self.coords = []  
    



class Builder(object):
    """
    Class for building natural neighbourhood visualisations.
    """

    def __init__(self, data_source):                
        """
        Constructor: requires a CSV file as argument.
        """
        
        self.data = []
        self.nn_dict = None
        self.nns = []
        self.nn_names = []
        self.colours = None
        
        self.fromCSV(data_source)
        self.neighbourhoods()
        
        
        
    def fromCSV(self, data_source, verbose=True):
        """
        Read in coordinate data from a CSV file
        """
        reader = csv.reader(open(data_source, "rU"))
        if verbose:
            print("Reading in the file '%s'\n" % data_source)
        next(reader)
        self.data = reader
        
            
    def add_points(self, verbose=True):
        """
        Build a dictionary that maps neighbourhood names into a list of
        coordinates, one for each survey response.
        """      
        d = defaultdict(list)
        for line in self.data:
            geo = tuple(map(float, line[4:6]))
            nn_name = self.standardise(line[2])
            d[nn_name].append(geo) 
        self.nn_dict = d
        self.nn_names = sorted(self.nn_dict.keys())
        if verbose:
            print("Building dictionary with %s keys\n" % len(d)) 
            
    def neighbourhoods(self):
        """
        Convert dictionary entries into Neighbourhood objects.
        """
        if self.nn_dict is None:
            self.add_points()
        if self.colours is None:
            self.colours_fromCSV(COLOURS)
        for name in self.nn_dict:
            nn = Neighbourhood(name)
            nn.coords = self.nn_dict[name]
            nn.centroid = tuple(np.mean(nn.coords, axis=0))
            if self.colours[nn.name] is not None:
                nn.colour = Color(self.colours[nn.name])
            else:
                nn.colour = Color(pick_for=nn.name)
            self.nns.append(nn)
        
        
    def standardise(self, name):
        """
        Convert a natural neighbourhood name into a standard format for
        filenames
        """
        name = name.lower()
        name = name.replace(" ", "_")
        name = name.replace("'", "")
        return name
    
    
    def colours_fromCSV(self, fn):
        d = {}
        with open(fn) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    (name, freq, colour) = row
                    name = self.standardise(name)
                    if colour == 'None':
                        colour = None
                    d[name] = colour
        self.colours = d
        
        
    
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
        count = 1
        
        for nn in self.nns:
            vals = nn.coords
            fn = os.path.join(subdir, nn.name + '.js')
            header = ("var %s = \n" % nn.name)
            contents = header + json.dumps(vals)
            with open(fn, "w") as outfile:
                outfile.write(contents)
                print("[%s] Writing to %s" % (count,fn))
            count = count + 1            
        
        #for nn in self.nn_dict:
            #vals = self.nn_dict[nn]          
            #fn = os.path.join(subdir, nn + '.js')
            #header = ("var %s = \n" % nn)
            #contents = header + json.dumps(vals)
            #with open(fn, "w") as outfile:
                #outfile.write(contents)
                #print("[%s] Writing to %s" % (count,fn))
            #count = count + 1
            

    def heat_params(self, nn):
        """
        Configure gradience and other parameters for the heatmap layer.
        """
        d = {}
        d['blur'] = 15
        d['radius'] = 28
        c = nn.colour
        c.set_saturation(1)
        
        d['gradient'] = {} 
        c.set_luminance(0.3)
        d['gradient'][0.4] = c.get_hex()
        c.set_luminance(0.5)
        d['gradient'][0.65] = c.get_hex()
        c.set_luminance(0.9)
        d['gradient'][1.0] = c.get_hex()
        return json.dumps(d)
    

    def js_headers(self):
        """
        Create a string representation of all the JS headers required.
        """        
        header_tmpl = '<script src="heatmap-data/%s.js" type="text/javascript"></script>'
        headers = [(header_tmpl % nn.name) for nn in self.nns]
        headers = "\n".join(headers)
        return headers
    
    def js_layers(self):
        layer_tmpl = """    var heatLayer%s = L.heatLayer(%s, %s).addTo(map);"""
        layers = [(layer_tmpl % (nn.name.capitalize(), nn.name, self.heat_params(nn))) for nn in self.nns]
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
    nns = Builder(CSV_IN)
    nns.dump_address_points(JS_OUT)
    nns.build_html(INDEX_OUT)

    
    
        
if __name__ == "__main__":
            main() 