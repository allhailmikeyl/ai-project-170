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

def sort_data(data):
    indices = np.lexsort((data[:, 1], data[:, 0], data[:, 2]))
    sorted_data = data[indices]

    return sorted_data

def assign_label(sorted_data, rice_type):
    m = 0
    sorted_label = []
    for i, row in enumerate(sorted_data):
        if i+1 == len(sorted_data):
            new_row = np.append(row, -1)
            sorted_label.append(new_row)
            break

        next_row = sorted_data[i+1]

        # Check first if the city in current row is the same city for the next row
        if row[2] == next_row[2]:
            # Compare the price of a given rice type
            if row[rice_type] > next_row[rice_type]:
                new_row = np.append(row, 1)
                sorted_label.append(new_row)
            else:
                new_row = np.append(row, 0)
                sorted_label.append(new_row)
        else:
            new_row = np.append(row, -1)
            sorted_label.append(new_row)

    return np.array(sorted_label)

def main():
    # Read csv file
    headers, data = read_file()

    # Sort the data by city and date
    sorted_data = sort_data(data)

    # Assign a target label (0 = down ; 1 = up)
    # Rice type indices = 4 - regular ; 5 - well-milled ; 6 - special
    sorted_label = assign_label(sorted_data, 4)

    for row in sorted_label:
        print(row)

    

main()