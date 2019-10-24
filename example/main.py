from example.server.service import User
from py_micro.py_grpc import MicroService

__all__ = ['User']


def run():
    MicroService.start()


if __name__ == '__main__':
    run()
