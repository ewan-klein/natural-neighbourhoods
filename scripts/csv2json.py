import csv
import geojson as geo

def normalise(reader):
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
            print l
        lat = float(lat)
        lng = float(lng)
        feature = geo.Feature(
        id = nn_id,
        geometry = geo.Point((lat, lng)),
        properties = {"nn": nn, "postcode": postcode}
        )
        features.append(feature)
        if verbose:
            print geo.dumps(feature)
    return features

def extract_nns(data):
    nns = []
    for l in data:
        nn = l[2]
        nns.append(nn)
    return sorted(set(nns))

def main():
    csv_in = "../survey_data_latlng.csv"       
    reader = csv.reader(open(csv_in, "rU"))
    reader.next()
    
    data = normalise(reader)
    features = lists2json(data)
    
    with open("../survey_data.json", "w") as json_out:
        geo.dump(geo.FeatureCollection(features), json_out)
    
    nns = extract_nns(data)
    print len(nns)
    for nn in nns:
        print nn

if __name__ == "__main__":
    main() 