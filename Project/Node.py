import csv
import os
import socket
import grpc
from concurrent import futures
import time
import re

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

nodes_info = {}
write_array = []
commit_counts = {}  # Stores the commit counters for each node
commit_counts[socket.gethostname()] = 0
leader_ip = None  # Stores the IP address of the current leader
last_heartbeat_time = time.time() 

# gRPC communication class
# --------------------------------------------------------------------------------------------------------------
class communicationHandlerServicer(Communication_pb2_grpc.communicationHandlerServicer):
    def WriteProcess(self, request, context):
        global write_array
        print()
        print(f"Proxy says: {request.data}")
        resendWriteToFollowers(request.data)
        fileName = re.search(r"INTO\s+(\w+)\s*\(", request.data)
        attributes = re.search(r"\((.*?)\)", request.data)
        writer(fileName.group(1), attributes.group(1), request.data)
        return Communication_pb2.WriteResponse(message="Write Request received by leader!")
    
    def ReadProcess(self, request, context):
        print()
        print(f"Proxy says: {request.key}")
        fileName = re.search(r"FROM\s+(\w+)\s+WHERE", request.key)
        attribute = re.search(r"WHERE\s+(\w+)\s*==", request.key)
        value = re.search(r"==\s*(\w+)", request.key)
        result = reader(fileName.group(1), attribute.group(1), value.group(1))
        return Communication_pb2.ReadResponse(data=result)
    
    def DisconnectionUpdate(self, request, context):
        global nodes_info
        nodes_info = request.nodes_info
        print(nodes_info)
        return Communication_pb2.GResponse(number = 1)
    
    def AppendEntries(self, request, context):
        print()
        print(f"Leader says: {request.data}")
        fileName = re.search(r"INTO\s+(\w+)\s*\(", request.data)
        attributes = re.search(r"\((.*?)\)", request.data)
        writer(fileName.group(1), attributes.group(1), request.data)
        return Communication_pb2.GResponse(number = 1)
    
    def UpdateWriteArray(self, request, context):
        global write_array
        print()
        print(f"New node says: {request.message}")
        return Communication_pb2.Array(array = write_array)
    
    def Heartbeat(self, request, context):
        print("Heartbeat received from leader")
        return Communication_pb2.GResponse(number=1)  # Acknowledge heartbeat
    
    # Method to handle new leader notification from the proxy
    def NewLeaderNotification(self, request, context):
        global leader_ip, nodes_info
        new_leader_ip = request.new_leader_ip
        print(f"Node received notification of new leader: {new_leader_ip}")
        
        # Update the local leader information
        leader_ip = new_leader_ip
        # Update all node roles locally
        for key in nodes_info.keys():
            nodes_info[key] = "follower"
        nodes_info[leader_ip] = "leader"
        
        return Communication_pb2.GResponse(number=1)


# Resend writing process from leader to followers
# --------------------------------------------------------------------------------------------------------------
def resendWriteToFollowers(data):
    print()
    for key, value in nodes_info.items():
        print(f"IP={key} | Role={value}")
        if value == "follower":
            #Append
            print()
            print(f"A follower has been detected with ip = {key}")
            try:
                with grpc.insecure_channel(f"{key}:50053") as channel:
                    stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                    response = stub.AppendEntries(Communication_pb2.WriteRequest(data = data))
            except grpc.RpcError as e:
                print(f"Failed to send append to follower at {key}: {e}")


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
                return f"Result for '{desiredValue}' in column '{attribute}':\n {results}"
            else:
                print()
                return f"No results found for '{desiredValue}' in column '{attribute}'"
    else:
        print()
        return "This file doesn't exists!"


# Write to CSV method
# --------------------------------------------------------------------------------------------------------------
def writer(name, attributes, statement):
    global write_array, commit_counts
    write_array.append(statement)
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
        
    # Increment the commit counter
    current_node = socket.gethostname()
    commit_counts[current_node] = commit_counts.get(current_node, 0) + 1
    print(f"Commit count for {current_node}: {commit_counts[current_node]}")


# Method to say to proxy that this node is online with a role and maintain the heartbeat
# --------------------------------------------------------------------------------------------------------------
def updateProxy(role):
    global nodes_info
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    with grpc.insecure_channel("54.158.59.187:50052") as channel:
        stub = Communication_pb2_grpc.communicationHandlerStub(channel)
        response = stub.UpdateNodes(Communication_pb2.UpdateInfoRequest(ip=IPAddr, role=role))
        nodes_info = response.nodes_info
        print()
        print(f"Local nodes hashmap: {nodes_info}")
            
    # Method to update new nodes' dbs
    for key, value in nodes_info.items():
        if value == "leader" and key != IPAddr:
            with grpc.insecure_channel(f"{key}:50053") as channel:
                stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                array = stub.UpdateWriteArray(Communication_pb2.ArrayRequest(message = f"Request for array from '{key}'"))
                if array.array:
                    if os.path.exists("Cars.csv"):
                        os.remove("Cars.csv")
                    print()
                    print("Restoring from leader's copy...")
                    for statement in array.array:
                        print()
                        print(f"Loading from Leader: {statement}")
                        fileName = re.search(r"INTO\s+(\w+)\s*\(", statement)
                        attributes = re.search(r"\((.*?)\)", statement)
                        writer(fileName.group(1), attributes.group(1), statement)


def notifyDisconnection():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    with grpc.insecure_channel("54.158.59.187:50052") as channel:
        stub = Communication_pb2_grpc.communicationHandlerStub(channel)
        response = stub.Disconnection(Communication_pb2.DisconnectionRequest(address=IPAddr))


def heartbeat():
    global nodes_info, last_heartbeat_time
    while True:
        leader_detected = False # Reset leader detection flag at the beginning of each cycle
        for key, value in nodes_info.items():
            if value == "leader":  # Check if there is a leader in the cluster
                leader_detected = True  # Mark that a leader is currently detected
                try:
                    with grpc.insecure_channel(f"{key}:50053") as channel:
                        stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                        response = stub.Heartbeat(Communication_pb2.GRequest(number=1))
                        print(f"Heartbeat sent to {key}, response: {response.number}")
                        last_heartbeat_time = time.time()  # Update the time of the last heartbeat received
                except grpc.RpcError as e:
                    print(f"Failed to send heartbeat to leader at {key}: {e}")
                    
        # If no heartbeat from the leader is detected within the last 10 seconds
        if leader_detected and time.time() - last_heartbeat_time > 10:
            print("Leader heartbeat timeout, starting new leader election...")
            chooseNewLeader()  # Start the new leader election process
            last_heartbeat_time = time.time()  # Reset the timer after electing a new leader

        time.sleep(5)  # Check for heartbeats every 5 seconds
     
     
# New Leader Election
# --------------------------------------------------------------------------------------------------------------
def chooseNewLeader(): 
    # Method for electing a new leader based on the number of commits
    global nodes_info, leader_ip, commit_counts

    # Finding follower nodes and their commit counter
    candidate = None
    max_commits = -1

    for key, value in nodes_info.items():
        if value == "follower":
            # Get the number of follower commits
            follower_commit_count = commit_counts.get(key, 0)  # Using the Accounting Dictionary
            if follower_commit_count > max_commits:
                max_commits = follower_commit_count
                candidate = key

    # If there is a candidate, declare the new leader
    if candidate:
        print(f"New leader elected: {candidate}")
        leader_ip = candidate
        # Update node roles
        for key in nodes_info.keys():
            nodes_info[key] = "follower"
        nodes_info[leader_ip] = "leader"
        
        updateLeaderIp(leader_ip)
        notifyNewLeaderToProxy(leader_ip)

def updateLeaderIp():
    global leader_ip, nodes_info
    for key, value in nodes_info.items():
        if value == "leader":
            leader_ip = key
            break  # Salir del bucle una vez que se encuentra el líder
        

# Notify the proxy about the new leader
# --------------------------------------------------------------------------------------------------------------
def notifyNewLeaderToProxy(new_leader_ip):
    # This method is responsible for notifying the proxy when a new leader is chosen.
    print(f"Notifying proxy that {new_leader_ip} is the new leader")
    
    try:
        with grpc.insecure_channel("54.158.59.187:50052") as channel:  # Connect to proxy (use actual proxy IP)
            stub = Communication_pb2_grpc.communicationHandlerStub(channel)
            response = stub.UpdateLeaderInfo(Communication_pb2.LeaderInfoRequest(new_leader_ip=new_leader_ip))
            print("Proxy notified of new leader.")
    except grpc.RpcError as e:
        print(f"Failed to notify proxy about new leader: {e}")


# Server configuration
# --------------------------------------------------------------------------------------------------------------
def serve():
    node = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Communication_pb2_grpc.add_communicationHandlerServicer_to_server(communicationHandlerServicer(), node)
    node.add_insecure_port('[::]:50053')    # This must have to be changed later, it is like this only for local tests
    if os.path.exists("Cars.csv"):
        os.remove("Cars.csv")
    node.start()
    # Start heartbeat thread using ThreadPoolExecutor
    executor = futures.ThreadPoolExecutor(max_workers=1)
    executor.submit(heartbeat)  # This will run heartbeat in a separate thread
    print()
    print("Node started on port 50053")
    updateProxy("follower")
    try:
        while True:
            time.sleep(86400)  # Keep server alive
    except KeyboardInterrupt:
        notifyDisconnection()
        node.stop(0)


# Main Method
# --------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    serve()