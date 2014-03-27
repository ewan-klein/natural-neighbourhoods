import csv
import geojson

def normalise(reader):
    new_rows = []
    for row in reader:
        nn = row[2]
        
        

def main():
    csv_in = "../survey_data_latlng.csv"       
    reader = csv.reader(open(csv_in, "rU"))
    reader.next()
    
    data = normalise(reader)
    
    json_out = "survey_data.json"


if __name__ == "__main__":
    main() 