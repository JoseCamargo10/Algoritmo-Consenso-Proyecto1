import raft
import csv
import os
import socket
import grpc
from concurrent import futures
import time

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

# gRPC communication class
# --------------------------------------------------------------------------------------------------------------
class communicationHandlerServicer(Communication_pb2_grpc.communicationHandlerServicer):
    def WriteProcess(self, request, context):
        print()
        print(f"Proxy says: {request.data}")
        return Communication_pb2.WriteResponse(message="Write Request received by leader!")
    
    def ReadProcess(self, request, context):
        print()
        print(f"Proxy says: {request.key}")
        return Communication_pb2.ReadResponse(data="Read Request received by leader!")


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
                print()
                print(f"Result for '{desiredValue}' in column '{attribute}':")
                for result in results:
                    print(result)
            else:
                print()
                print(f"Not finded results for '{desiredValue}' in column '{attribute}'")
    else:
        print()
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


# Method to say to proxy that this node is online with a role
# --------------------------------------------------------------------------------------------------------------
def updateProxy(role):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    with grpc.insecure_channel("localhost:50052") as channel:
        stub = Communication_pb2_grpc.communicationHandlerStub(channel)
        response = stub.UpdateNodes(Communication_pb2.UpdateInfoRequest(ip=IPAddr, role=role))
        print()
        print(f"Proxy says: {response.response}")


# Server configuration
# --------------------------------------------------------------------------------------------------------------
def serve():
    node = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Communication_pb2_grpc.add_communicationHandlerServicer_to_server(communicationHandlerServicer(), node)
    node.add_insecure_port('[::]:50053')    # This must have to be changed later, it is like this only for local tests
    node.start()
    print()
    print("Node started on port 50053")
    updateProxy("leader")
    try:
        while True:
            time.sleep(86400)  # Keep server alive
    except KeyboardInterrupt:
        node.stop(0)


# Main Method
# --------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    '''writer("Cars", "Chevrolet,USA,1980")
    writer("Cars", "Ferrari,Italy,1980")
    reader("Cars", "Year", "1980")'''
    serve()
