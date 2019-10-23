from example.proto import user_pb2_grpc, user_pb2
from py_grpc import MicroService


@MicroService.register(user_pb2_grpc.add_UserServicer_to_server, 'user.user')
class User:
    @classmethod
    def GetUser(self, request, context):
        user_id = request.user_id
        print(request)
        return user_pb2.UserModel(user_id=user_id, user_name='jiangxuewen', password='123456')

    @classmethod
    def PutUser(self, request, context):
        print(request)
        return user_pb2.Request(user_id=request.user_id)