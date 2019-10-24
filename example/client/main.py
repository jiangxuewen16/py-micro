from example.client import user
from example.proto import user_pb2


def run():
    a = user.GetUser(user_pb2.Request(user_id=2))
    print(a)


if __name__ == '__main__':
    run()
