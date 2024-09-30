import grpc
from concurrent import futures
import time

# Importa los archivos generados
import test_pb2
import test_pb2_grpc

# Implementa el servicio Greeter
class GreeterServicer(test_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return test_pb2.HelloReply(message=f'Hello, {request.name}!')

# Configura el servidor
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)  # Mantiene el servidor corriendo
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    server()
