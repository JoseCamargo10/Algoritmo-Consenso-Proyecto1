import grpc
from concurrent import futures
import time

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

# Method to send writing to leader
# --------------------------------------------------------------------------------------------------------------
def sendWrite(message):
    print(f"Write: {message}")


# Method to send reading to follower
# --------------------------------------------------------------------------------------------------------------
def sendRead(message):
    print(f"Read: {message}")


# gRPC communication class
# --------------------------------------------------------------------------------------------------------------
class communicationHandlerServicer(Communication_pb2_grpc.communicationHandlerServicer):
    def Client_Proxy(self, request, context):
        if request.message.startswith("INSERT"):
            sendWrite(request.message)
        elif request.message.startswith("SELECT"):
            sendRead(request.message)
        return Communication_pb2.Response(message="Statement received!")


# Server configuration
# --------------------------------------------------------------------------------------------------------------
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Communication_pb2_grpc.add_communicationHandlerServicer_to_server(communicationHandlerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)  # Keep server alive
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()