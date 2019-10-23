from example.proto import user_pb2_grpc
from py_grpc import MicroService


@MicroService.consume('user.user', user_pb2_grpc.UserStub)
def GetUser():
    pass
