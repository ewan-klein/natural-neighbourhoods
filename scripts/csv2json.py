"""
Convert the CSV-formatted geocoded survey data file into geoJSON.
"""
from __future__ import print_function

import colorsys
import csv
import geojson as geo
from collections import Counter


CSV_IN = "../survey_data_latlng.csv"
CSV_FILT = "../survey_data_latlng_filtered.csv"
JSON_OUT = "../survey_data.json"
NNS = "../nn_freq.csv"


def normalise_nns(reader):
    """
    Normalise neighbourhood names by removing slashes and removing 'Not supplied' values.
    """
    new_rows = []
    for row in reader:
        nn = row[2]
        if nn == "NN not supplied" or 'Edinburgh' in nn:
            continue
        nns = nn.split('/')
        if len(nns) > 1:
            for nn in nns[1:]:
                row[2] = nn
                new_rows.append(row)
        else:
            new_rows.append(row)
    return new_rows

        
def upper_postcode(line):
    """
    Ensure postcodes are all upper case.
    """
    postcode = line[3]
    line[3] = postcode.upper()
    return line


def filter_names(line, verbose=True):
    nn = line[2]
    parts = nn.split()
    old = nn
    if len(parts) > 1:
        if parts[0] in ['Granton', 'Baberton', 'Colinton']:
            nn = parts[0]
        if parts[0] in ['North', 'South'] and parts[1] != 'Queensferry':
            nn = parts[1]
        if parts[1] == 'Pilton':
            nn = parts[1]
        if parts[1] in ['Colonies', 'Park', 'Village', 'Hill', 'Avenue', 'Station', 'Terrace'] and parts[0] not in ['Dean', 'Church']:
            nn = parts[0]        
    if nn in ['Grange', 'Gyle']: 
        nn = 'The ' + nn
    line[2] = nn
    if verbose and nn != old:
        print("Replacing %s with %s" % (old, nn))
    return line

def filter_rare(line, counter, n=10, verbose=False):
    nn = line[2]
    if counter[nn] < n:
        if verbose:
            print('Skipping %s with count %s' % (nn, counter[nn]))
        return False
    return True

def lists2json(data, verbose=False):
    features = []
    for l in data:
        try:
            (nn_id, src, nn, postcode, lat, lng) = tuple(l)
        except ValueError:
            print(l)
        lat = float(lat)
        lng = float(lng)
        feature = geo.Feature(
        id = nn_id,
        geometry = geo.Point((lat, lng)),
        properties = {"nn": nn, "postcode": postcode}
        )
        features.append(feature)
        if verbose:
            print(geo.dumps(feature))
    return features

def colorize(nns):
    N = len(nns)
    
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = [colorsys.hsv_to_rgb(*hsv) for hsv in HSV_tuples]
    HEX_tuples = ['%02x%02x%02x' % (int(r*256), int(g*256), int(b*256)) for (r, g, b) in RGB_tuples]
    return HEX_tuples
    

def main():
    
    reader = csv.reader(open(CSV_IN, "rU"))
    reader.next()
    header = ['Record ID', 'Data Source', 'Allocated NN', 'Postcode', 'Latitude', 'Longitude']
    
    data = normalise_nns(reader)
    nns = [line[2] for line in data]
    print(len(nns))
    counter = Counter(nns)
    
    with open(NNS, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(counter.most_common())    
    
    data = [upper_postcode(l) for l in data]
    data = [filter_names(l) for l in data]
    data = [l for l in data if filter_rare(l, counter)]
    
    filtered_nns= sorted(set([line[2] for line in data]))
    print(len(filtered_nns))
    colors = colorize(filtered_nns)
    
    with open(CSV_FILT, "w") as outfile:
        lines = len(data)
        print('Dumping CSV with %s lines to %s' % (lines, CSV_FILT))
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(data)        
   
    features = lists2json(data)
    
    with open(JSON_OUT, "w") as outfile:
        print('Dumping GeoJSON to %s' % JSON_OUT)
        geo.dump(geo.FeatureCollection(features), outfile)    
    
    

if __name__ == "__main__":
    main() 