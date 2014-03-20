import csv
from postcodes import PostCoder



def main():
    csv_in = "Survey Data.csv"
    csv_out = "nn.csv"
    
    reader = csv.reader(open(csv_in, "rU"))
    for row in reader:
        #(record_id, data_source,allocated_NN,postcode, Xcord, Ycord , last_Modified, geography)
        data = list(row)[0:4]
        postcode = data[3]
        pc = PostCoder()
        result = pc.get(postcode)
        print result['geo']
        
        #try:
            #(record_id, data_source,allocated_NN,postcode, Xcord, Ycord , last_Modified, geography) = tuple(row)
        #except ValueError:
            #print row
            
        #new = ['Record Id','Data Source','Allocated NN','Pcode']

if __name__ == "__main__":
    main() 