import time
from collections import namedtuple

import grpc
from concurrent import futures

_HOST = '127.0.0.1'
_PORT = '8111'

server_register = namedtuple('server_register', 'add_server server_class service_code')


class Producer(object):
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    service_list = []

    def __init__(self, max_workers=4):
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers))

    def set_service(self, service_list: list):
        for service in service_list:
            # todo: 这里做服务注册， 怎么做服务健康检查 register
            # user_pb2_grpc.add_UserServicer_to_server(User(), grpcServer)
            service['add_server'](service['server_class'], self.grpc_server)
        return self

    def start(self, host=None, port=None, ):
        host = host or _HOST
        port = port or _PORT
        self.grpc_server.add_insecure_port(host + ':' + port)
        self.grpc_server.start()
        try:
            while True:
                time.sleep(self._ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.grpc_server.stop(0)


class Consumer(object):
    def __init__(self, service_code):
        # todo:从cousul拿取服务地址 address + port
        self.service_code = service_code

        service_addr = consul.getByCode(service_code)
        self.address = service_addr.address or _HOST
        self.port = service_addr.port or _PORT
        self.conn = grpc.insecure_channel(self.address + ':' + self.port)

        pass

    def do(self, ):
        client = user_pb2_grpc.UserStub(channel=self.conn)

        self.conn

