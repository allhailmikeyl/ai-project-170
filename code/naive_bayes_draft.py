import csv
import numpy as np
from datetime import datetime

csv_file = "../data/rice_per_weather.csv"

def read_file():
    headers = None
    rows_data = []
    with open(csv_file, "r") as f:
        data = csv.reader(f)
        for i, row in enumerate(data):
            # Line 1 (index 0) consists of the headers
            if i == 0: 
                headers = np.array(row)
            else:
                # Convert the year into int
                row[0] = int(row[0])
                # Convert the month name to its integer equivalent
                row[1] = datetime.strptime(row[1], "%B").month 
                # Convert the data values to float
                row[4:] = [float(x) if x else 0 for x in row[4:]]

                rows_data.append(row)
    
    return headers, np.array(rows_data, dtype=object)

def main():
    # Read csv file
    headers, data = read_file()

main()