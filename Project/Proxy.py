import grpc
from concurrent import futures
import time

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

nodes_info = {}
read_index = 0

# gRPC communication class
# --------------------------------------------------------------------------------------------------------------
class communicationHandlerServicer(Communication_pb2_grpc.communicationHandlerServicer):
    def Client_Proxy(self, request, context):
        if request.message.startswith("INSERT"):
            sendWrite(request.message)
        elif request.message.startswith("SELECT"):
            readResponse = sendRead(request.message)
            return Communication_pb2.Response(message=readResponse)
        return Communication_pb2.Response(message="Statement received!")
    
    def UpdateNodes(self, request, context):
        nodes_info[request.ip] = request.role
        print()
        print(nodes_info)
        disconnectionOrconnectionUpdate()
        return Communication_pb2.UpdateInfoResponse(nodes_info = nodes_info)
    
    def Disconnection(self, request, context):
        del nodes_info[request.address]
        print(nodes_info)
        if nodes_info.items():
            disconnectionOrconnectionUpdate()
        return Communication_pb2.DisconnectionResponse(message="1")

    # gRPC method to update leader information in the proxy
    def UpdateLeaderInfo(self, request, context):
        new_leader_ip = request.new_leader_ip
        print(f"Received request to update leader to {new_leader_ip}")
        
        # Update the nodes_info hashmap with the new leader
        for key,value in nodes_info.items():
            nodes_info[key] = "follower"
        nodes_info[new_leader_ip] = "leader"
        
        # Propagate the new leader information to all followers
        propagateLeaderUpdate(new_leader_ip)
        return Communication_pb2.GResponse(number=1)


# Method to propagate the leader update to all nodes
# --------------------------------------------------------------------------------------------------------------
def propagateLeaderUpdate(new_leader_ip):
    for key, value in nodes_info.items():
        if key != new_leader_ip:  # Send to followers only
            try:
                with grpc.insecure_channel(f"{key}:50053") as channel:
                    stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                    stub.NewLeaderNotification(Communication_pb2.LeaderNotificationRequest(new_leader_ip=new_leader_ip))
                    print(f"Notified follower {key} about new leader {new_leader_ip}.")
            except grpc.RpcError as e:
                print(f"Failed to notify follower at {key}: {e}")


# Method to alert other nodes about the disconnection of one node or connection of a new one
# --------------------------------------------------------------------------------------------------------------
def disconnectionOrconnectionUpdate():
    for key, value in nodes_info.items():
        try:
            with grpc.insecure_channel(f"{key}:50053") as channel:
                stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                response = stub.DisconnectionUpdate(Communication_pb2.UpdateInfoResponse(nodes_info = nodes_info))
        except grpc.RpcError as e:
            print(f"Error updating node {key}: {e}")


# Method to record heartbeat of the leader
# --------------------------------------------------------------------------------------------------------------
def Heartbeat(self, request, context):
    print("Received heartbeat from leader")
    return Communication_pb2.GResponse(number=1)  # Acknowledge heartbeat


# Method to send writing to leader
# --------------------------------------------------------------------------------------------------------------
def sendWrite(message):
    print()
    print(f"Write: {message}")
    for key, value in nodes_info.items():
        if value == "leader":
            # Resend the message to leader
            with grpc.insecure_channel(f"{key}:50053") as channel:
                stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                response = stub.WriteProcess(Communication_pb2.WriteRequest(data = message))
                print()
                print(f"Leader says: {response.message}")


# Method to send reading to follower
# --------------------------------------------------------------------------------------------------------------
def sendRead(message):
    global read_index
    print()
    print(f"Read: {message}")

    # Filtering only by followers
    followers = [key for key, value in nodes_info.items() if value == "follower"]
    if not followers:
        return "No followers available for this read request!"
    
    selected_follower = followers[read_index % len(followers)]  # Round Robin to select the follower
    read_index += 1     # Next follower to next request
    print(f"Sending read request to follower at {selected_follower}")

    try:
        with grpc.insecure_channel(f"{selected_follower}:50053") as channel:
            stub = Communication_pb2_grpc.communicationHandlerStub(channel)
            response = stub.ReadProcess(Communication_pb2.ReadRequest(key = message))
            print()
            return response.data
    except grpc.RPCError as e:
        print(f"Failed to send read to follower at {selected_follower}: {e}")
        return "Read request failed."


# Server configuration
# --------------------------------------------------------------------------------------------------------------
def serve():
    proxy = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Communication_pb2_grpc.add_communicationHandlerServicer_to_server(communicationHandlerServicer(), proxy)
    proxy.add_insecure_port('[::]:50051')
    proxy.add_insecure_port('[::]:50052')
    proxy.start()
    print()
    print("Proxy started on port 50051 and 50052")
    try:
        while True:
            time.sleep(86400)  # Keep server alive
    except KeyboardInterrupt:
        proxy.stop(0)


# Main Method
# --------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    serve()