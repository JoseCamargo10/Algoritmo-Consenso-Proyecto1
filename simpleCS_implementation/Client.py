import grpc

# Importa los archivos generados
import test_pb2
import test_pb2_grpc

def run():
    # Conecta al servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.GreeterStub(channel)
        
        # Realiza una solicitud SayHello
        response = stub.SayHello(test_pb2.HelloRequest(name='Mario'))
        print(f"Greeter client received: {response.message}")

if __name__ == '__main__':
    run()
