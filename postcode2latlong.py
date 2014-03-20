"""
Convert survey data gridrefs into latlong.
"""

import csv
from postcodes import PostCoder
LAST = 3091.0


def main():
    csv_in = "Survey Data.csv"
    
    
    reader = csv.reader(open(csv_in, "rU"))
    #(record_id, data_source,allocated_NN,postcode, Xcord, Ycord , last_Modified, geography)
    reader.next() #skip header
    new_rows = []
    for row in reader:       
        data = list(row)[0:4]
        postcode = data[3]
        pc = PostCoder()
        gdict = pc.get(postcode)
        cur = int(data[0]) 
        percent = (cur/LAST) * 100
        print ("%f" % (percent)) + "%"
        lat = gdict['geo']['lat']
        lng = gdict['geo']['lng']
        new_row = data.extend([lat, lng])
        new_rows.append(new_row)
        
        
    with open ('nn.csv', mode='r') as csv_out:
        writer = csv.writer(csv_out, dialect='excel')
        for row in new_rows:
            writer.writerow(row)
         

if __name__ == "__main__":
    main() 