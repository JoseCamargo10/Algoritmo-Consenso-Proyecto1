import grpc
import time

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

def read():
    print("Write the parameters to read with this structure:")
    print("SELECT * FROM {csv_name} WHERE ID = {id}")
    request = input()
    print(request)
    # Connect to server (in this case, to proxy)
    #with grpc.insecure_channel("localhost:50051") as channel:   # Here we must change with ip adress and port for AWS
        #stub = Communication_pb2_grpc.communicationHandler(channel)

def write():
    print()

def runClient():
    # Makes a request
    action = input("Which action do you want to execute?: ")
    if action == "read":
        read()
    elif action == "write":
        print(f"2. {action}")

if __name__ == '__main__':
    print()
    print("Welcome to Chema and Valencia's project!")
    print("Here, you can write and read into a CSV file, stored in a cluster!")
    print()
    runClient()