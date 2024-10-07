import raft
import csv
import os

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

# Read from CSV method
# --------------------------------------------------------------------------------------------------------------
def reader(name, attribute, desiredValue):
    fileName = f"{name}.csv"
    if os.path.exists(fileName):
        with open (fileName, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            results= []

            for row in reader:
                if row[attribute] == desiredValue:
                    results.append(row)
            
            if results:
                print(f"Result for '{desiredValue}' in column '{attribute}':")
                for result in results:
                    print(result)
            else:
                print(f"Not finded results for '{desiredValue}' in column '{attribute}'")
    else:
        print("This file doesn't exists!")


# Write to CSV method
# --------------------------------------------------------------------------------------------------------------
def writer(name, attributes):
    headers = [["Brand", "Country", "Year"]]
    fileName = f"{name}.csv"

    if not os.path.exists(fileName):
        with open (fileName, mode='w', newline='') as csvfile:
            firstwriter = csv.writer(csvfile)
            firstwriter.writerows(headers)
    
    attributes_list = [attributes.split(",")]
    with open (fileName, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(attributes_list)


if __name__ == '__main__':
    writer("Cars", "Chevrolet,USA,1980")
    writer("Cars", "Ferrari,Italy,1980")
    reader("Cars", "Year", "1980")