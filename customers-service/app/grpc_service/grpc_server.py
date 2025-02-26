import logging
from concurrent import futures

import grpc
from app.core.repository import customers_repo
from app.grpc_service import service_pb2, service_pb2_grpc
from app.utils import get_logger

logger = get_logger(__file__, log_level=logging.DEBUG)


class CustomerService(service_pb2_grpc.CustomerServiceServicer):
    def GetCustomer(self, request, context):
        customer = customers_repo.get_customer(customer_id=request.customer_id)
        exists = True if customer else False
        return service_pb2.CustomerResponse(exists=exists)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
