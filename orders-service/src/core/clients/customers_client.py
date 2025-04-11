import grpc
from src.grpc_service import service_pb2, service_pb2_grpc


class CustomersClient:
    def check_customer_exists(self, customer_id):
        try:
            channel = grpc.insecure_channel("customer-service:50051")
            stub = service_pb2_grpc.CustomerServiceStub(channel)
            request = service_pb2.CustomerRequest(customer_id=customer_id)
            response = stub.GetCustomer(request)

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise RuntimeError("The customer-service is unavailable")
            elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                raise TimeoutError("Request to customer-service timed out")
            else:
                raise RuntimeError(f"gRPC error: {e.code()} - {e.details()}")

        else:
            return response.exists
