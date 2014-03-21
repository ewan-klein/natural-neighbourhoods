"""
Convert survey data gridrefs into latlong.
"""

import csv
from postcodes import PostCoder



def main():
    FIRST = 1256
    LAST = 3091.0  
    csv_in = "Survey Data.csv"       
    reader = csv.reader(open(csv_in, "rU"))
    
    #(record_id, data_source,allocated_NN,postcode, Xcord, Ycord , last_Modified, geography)
    reader.next() #skip header
    new_rows = []
    for row in reader:       
        data = list(row)[0:4]
        cur = int(data[0])                
        if cur < FIRST:
            continue 
        postcode = data[3]
        pc = PostCoder()
        gdict = pc.get(postcode)
        try:
            lat = gdict['geo']['lat']
            lng = gdict['geo']['lng']
            data.extend([lat, lng])
            percent = (cur/LAST) * 100
            print ("%s [%f" % (cur, percent)) + "%]"                   
            FIRST = FIRST + 1
        except TypeError:
            print "Failed to geo-code"
        #new_rows.append(new_row)
        
        
        with open('nn.csv', mode='a') as csv_out:
            writer = csv.writer(csv_out, dialect='excel')
            #for row in new_rows:
            writer.writerow(data)
         

if __name__ == "__main__":
    main() 