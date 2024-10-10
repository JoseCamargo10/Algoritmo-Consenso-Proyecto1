import grpc
from concurrent import futures
import time

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

nodes_info = {}

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
        return Communication_pb2.UpdateInfoResponse(nodes_info = nodes_info)
    
    def Disconnection(self, request, context):
        del nodes_info[request.address]
        print(nodes_info)
        return Communication_pb2.DisconnectionResponse(message="1")


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
    print()
    print(f"Read: {message}")
    for key, value in nodes_info.items():
        if value == "follower":
            # Resend the message to leader
            with grpc.insecure_channel(f"{key}:50053") as channel:
                stub = Communication_pb2_grpc.communicationHandlerStub(channel)
                response = stub.ReadProcess(Communication_pb2.ReadRequest(key = message))
                print()
                return response.data


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