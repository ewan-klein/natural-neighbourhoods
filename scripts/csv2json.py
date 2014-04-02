"""
Convert the CSV-formatted geocoded survey data file into geoJSON.
"""
from __future__ import print_function

import csv
import geojson as geo
from collections import Counter


CSV_IN = "../survey_data_latlng.csv"
JSON_OUT = "../survey_data.json"
NNS = "../nn_freq.csv"

def unslash(reader):
    """
    Normalise neighbourhood names by removing slashes.
    """
    new_rows = []
    for row in reader:
        nn = row[2]
        if nn == "NN not supplied":
            continue
        nns = nn.split('/')
        if len(nns) > 1:
            for nn in nns[1:]:
                row[2] = nn
                new_rows.append(row)
        else:
            new_rows.append(row)
    return new_rows

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

def nns_info(nns, outfile=True):
    c = Counter(nns)
    freqdist = c.most_common()
    with open(NNS, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(freqdist)

def main():
    
    reader = csv.reader(open(CSV_IN, "rU"))
    reader.next()
    
    data = unslash(reader)
    features = lists2json(data)
    
    with open(JSON_OUT, "w") as outfile:
        geo.dump(geo.FeatureCollection(features), outfile)
    
    nns = extract_nns(data)
    nns_info(nns)
    
    #print(len(nns))
    #for nn in nns:
        #print(nn)

if __name__ == "__main__":
    main() 