import socket
import time
from collections import namedtuple
from operator import methodcaller
from types import FunctionType

import grpc
from concurrent import futures

from example.proto import user_pb2
from py_consul import ConsulMicroServer

server_register = namedtuple('server_register', 'service_code add_server server_class method stub req_msg')


class MicroService(object):
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    """配置"""
    START_SERVER = True
    MAX_WORKERS = 4
    HOST = '127.0.0.1'
    PORT = 8111
    APP_NAME = ''
    REG_HOST = '118.126.105.239'
    REG_PORT = 8500

    _SERVICE_LIST = []
    _GRPC_SERVER = grpc.server(futures.ThreadPoolExecutor(MAX_WORKERS))
    _CONSUL_SERVER = ConsulMicroServer(REG_HOST, REG_PORT)

    """注册服务->装饰器方法"""

    @classmethod
    def register(cls, servicer_func: FunctionType, service_name: str, tags=None):
        print(servicer_func)

        def my_decorator(func):
            # 如果开启服务注册，则自动注册
            if cls.START_SERVER:
                if not isinstance(servicer_func, FunctionType):
                    raise Exception("微服务注册，必须是方法!")

                # 添加需要注册的服务
                servicer_func(func(), cls._GRPC_SERVER)
                cls._CONSUL_SERVER.reg_service(service_name, cls.HOST, cls.PORT, tags)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return my_decorator

    """服务消费逻辑"""

    @classmethod
    def consume(cls, service_code, stub, ):
        service_addr = cls._CONSUL_SERVER.get_service(service_code)
        host = service_addr[0]
        port = service_addr[1]
        conn = grpc.insecure_channel(host + ':' + str(port))
        client = stub(channel=conn)
        return client.GetUser(user_pb2.Request(user_id=2))

    """启动微服务生产者"""

    @classmethod
    def start(cls):
        cls._GRPC_SERVER.add_insecure_port(cls.HOST + ':' + str(cls.PORT))
        cls._GRPC_SERVER.start()
        try:
            while True:
                time.sleep(cls._ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            cls._GRPC_SERVER.stop(0)


"""获取本机ip"""


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# class Producer(object):
#     _ONE_DAY_IN_SECONDS = 60 * 60 * 24
#
#     def __init__(self, host, port, max_workers=4):
#         self.host = host or _HOST
#         self.port = port or _PORT
#         self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers))
#
#     """设置要注册的服务"""
#
#     def set_service(self, service_list: list):
#         for service in service_list:
#             # todo: 这里做服务注册， 怎么做服务健康检查 register
#             # user_pb2_grpc.add_UserServicer_to_server(User(), grpcServer)
#             # ConsulMicroServer.reg_service()
#             service['add_server'](service['server_class'], self.grpc_server)
#         return self
#
#     """启动服务"""
#
#     def start(self):
#         self.grpc_server.add_insecure_port(self.host + ':' + self.port)
#         self.grpc_server.start()
#         try:
#             while True:
#                 time.sleep(self._ONE_DAY_IN_SECONDS)
#         except KeyboardInterrupt:
#             self.grpc_server.stop(0)
#
#
# class Consumer(object):
#     def __init__(self, service_code):
#         # todo:从cousul拿取服务地址 address + port
#         self.service_code = service_code
#
#         service_addr = ConsulMicroServer.get_service(service_code)
#
#         self.address = service_addr[0] or _HOST
#         self.port = service_addr[0] or _PORT
#
#         self.stub = service_addr.
#         self.req_msg =
#         self.method = ''
#         self.conn = grpc.insecure_channel(self.address + ':' + self.port)
#
#     def do(self, request):
#         stub = self.stub(channel=self.conn)
#         return methodcaller(self.method(), self.req_msg(request))(stub)  # todo:xxxxxx
