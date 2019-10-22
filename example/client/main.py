from example.proto import user_pb2_grpc
from py_grpc import MicroService


def run():
    resonse = MicroService.consume('user.user', user_pb2_grpc.UserStub)
    print(resonse)


if __name__ == '__main__':
    run()
