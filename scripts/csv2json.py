"""
Convert the CSV-formatted geocoded survey data file into geoJSON.
"""
from __future__ import print_function

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
    postcode = line[3]
    line[3] = postcode.upper()
    return line


def filter_names(line, verbose=True):
    nn = line[2]
    parts = nn.split()
    new = nn
    if len(parts) > 1:
        new = nn
        if parts[0] in ['Granton', 'Baberton']:
            new = parts[0]
        if parts[0] in ['North', 'South'] and parts[1] != 'Queensferry':
            new = parts[1]
        if parts[1] in ['Colonies', 'Park', 'Village', 'Hill', 'Avenue', 'Station', 'Terrace'] and parts[0] not in ['Dean', 'Church']:
            new = parts[0]
        line[2] = new
    if new in ['Grange', 'Gyle']: 
        new = 'The ' + new
    if verbose and nn != new:
        print("Replacing %s with %s" % (nn, new))
    return line

def filter_rare(line, counter, n=10, verbose=True):
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

def extract_nns(data):
    """
    Pull out the natural neighbourhood names
    """
    nns = []
    for l in data:
        nn = l[2]
        nns.append(nn)
    return nns



def main():
    
    reader = csv.reader(open(CSV_IN, "rU"))
    reader.next()
    
    data = normalise_nns(reader)
    nns = extract_nns(data)
    counter = Counter(nns)
    
    with open(NNS, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(counter.most_common())    
    
    fixed_postcodes = [upper_postcode(l) for l in data]
    filtered = [filter_names(l) for l in fixed_postcodes]
    thresholded = [l for l in filtered if filter_rare(l, counter)]
    
    with open(CSV_FILT, "w") as outfile:
        lines = len(thresholded)
        print('Dumping CSV with %s lines to %s' % (lines, CSV_FILT))
        writer = csv.writer(outfile)
        writer.writerows(thresholded)        
   
    features = lists2json(thresholded)
    
    with open(JSON_OUT, "w") as outfile:
        print('Dumping GeoJSON to %s' % JSON_OUT)
        geo.dump(geo.FeatureCollection(features), outfile)    
    
    

if __name__ == "__main__":
    main() 