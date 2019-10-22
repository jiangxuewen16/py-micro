from py_grpc import MicroService
from example.server.service import User

__all__ = ['User']


def run():
    MicroService.start()


if __name__ == '__main__':
    run()
