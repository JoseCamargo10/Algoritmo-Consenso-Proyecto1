import grpc
import re

# Import generated files (for gRPC communication)
import Communication_pb2
import Communication_pb2_grpc

# Send message to proxy
# --------------------------------------------------------------------------------------------------------------
def write(statement):
    print(statement)
     # Connect to server (in this case, to proxy)
    with grpc.insecure_channel("3.89.158.169:50051") as channel:   # Here we must change with ip adress and port for AWS
        stub = Communication_pb2_grpc.communicationHandlerStub(channel)

        response = stub.Client_Proxy(Communication_pb2.Request(message=statement))
        print(f"Server says: {response.message}")


def read(statement):
    print(statement)
    # Connect to server (in this case, to proxy)
    with grpc.insecure_channel("3.89.158.169:50051") as channel:   # Here we must change with ip adress and port for AWS
        stub = Communication_pb2_grpc.communicationHandlerStub(channel)

        response = stub.Client_Proxy(Communication_pb2.Request(message=statement))
        print(f"Server says: {response.message}")


# Validation statement methods
# --------------------------------------------------------------------------------------------------------------
def validate_write(statement):
    pattern = r"INSERT INTO \w+ \((\w+,?\s?)+\)"
    match = re.match(pattern, statement.strip())

    if not match:
        return False, "Invalid SELECT syntax. Correct format is: INSERT INTO table_name (brand,country,year)"
    return True, "Valid INSERT statement."

def validate_read(statement):
    pattern = r"SELECT \* FROM \w+ WHERE \w+ == .+"
    match = re.match(pattern, statement.strip())

    if not match:
        return False, "Invalid SELECT syntax. Correct format is: SELECT * FROM table_name WHERE attribute == desired_value"
    return True, "Valid SELECT statement."


# RunClient Method to receive statement
# --------------------------------------------------------------------------------------------------------------
def runClient():
    print("To write into database, try the following structure:")
    print("INSERT INTO table_name (brand,country,year)")
    print()
    print("To read a value in database, try the following structure:")
    print("SELECT * FROM table_name WHERE attribute == desired_value")
    print()
    statement = input("Enter your statement: ").strip()

    if statement.startswith("INSERT"):
        valid, message = validate_write(statement)
        print(message)
        print()
        write(statement)
    elif statement.startswith("SELECT"):
        valid, message = validate_read(statement)
        print(message)
        print()
        read(statement)
    else:
        print("Invalid statement. Please try again.")


# Main Method
# --------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print()
    print("Welcome to Chema and Valencia's project!")
    print("Here, you can write and read into a CSV file, stored in a cluster!")
    print("In this CSV you have the information of cars by their id, brand, country and year of creation")
    print()
    runClient()