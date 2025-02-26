import grpc
from src.grpc_service import service_pb2, service_pb2_grpc


class CustomersClient:
    def check_customer_exists(self, customer_id):
        channel = grpc.insecure_channel("customer-service:50051")
        stub = service_pb2_grpc.CustomerServiceStub(channel)
        request = service_pb2.CustomerRequest(customer_id=customer_id)
        response = stub.GetCustomer(request)
        return response.exists
