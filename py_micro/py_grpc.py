import socket
import time
from operator import methodcaller
from types import FunctionType

import grpc
from concurrent import futures

from py_micro.py_consul import ConsulMicroServer


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

    _INSECURE_CHANNEL_LIST = []  # grpc 连接池
    _SERVICE_LIST = []
    _GRPC_SERVER = grpc.server(futures.ThreadPoolExecutor(MAX_WORKERS))
    _CONSUL_SERVER = ConsulMicroServer(REG_HOST, REG_PORT)

    """注册服务->装饰器方法"""

    @classmethod
    def register(cls, servicer_func: FunctionType, service_name: str = None):
        def my_decorator(func):
            # 如果开启服务注册，则自动注册
            if cls.START_SERVER:
                if not isinstance(servicer_func, FunctionType):
                    raise Exception("微服务注册，必须是方法!")

                ob = func()
                # 添加需要注册的服务
                servicer_func(ob, cls._GRPC_SERVER)
                # 注册所有方法列表
                tags = list(
                    filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(ob, m)),
                           dir(ob)))
                cls._CONSUL_SERVER.reg_service(service_name, cls.HOST, cls.PORT, tags)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return my_decorator

    """服务消费逻辑"""

    @classmethod
    def consume(cls, service_id, stub, server_name: str = None):
        def my_decorator(func):
            def wrapper(*args, **kwargs):
                service_addr = cls._CONSUL_SERVER.get_service(service_id)
                host = service_addr[0]
                port = service_addr[1]
                tags = service_addr[2]
                method = server_name or func.__name__
                if method not in tags:
                    raise Exception('服务方法不存在')

                conn = grpc.insecure_channel("{0}:{1}".format(host, port))  # todo:这个可以维护一个连接池
                client = stub(channel=conn)

                if args:
                    param = args[0]
                elif kwargs:
                    param = list(kwargs.values())[0]
                else:
                    raise Exception('参数不存在')
                return methodcaller(method, param)(client)  # 自调方法

            return wrapper

        return my_decorator

    """启动微服务"""

    @classmethod
    def start(cls):
        cls._GRPC_SERVER.add_insecure_port("{0}:{1}".format(cls.HOST, cls.PORT))
        cls._GRPC_SERVER.start()
        try:
            while True:
                time.sleep(cls._ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            cls._GRPC_SERVER.stop(0)


# class GrpcConnPool(object):
#     _POOL: dict = []
#
#     @classmethod
#     def pop(cls, host, port):
#         addr = "{0}:{1}".format(host, port)
#         if addr in cls._POOL:
#
#         conn = grpc.insecure_channel("{0}:{1}".format(host, port))  # todo:这个可以维护一个连接池
#         pass
#
#     @classmethod
#     def push(cls, host, port):

