import hashlib

import consul


class ConsulMicroServer(object):
    def __init__(self, host, port):

        """初始化，连接consul服务器"""
        self._consul = consul.Consul(host, port)

    def reg_service(self, name: str, host, port, tags=None):
        tags = tags or []

        service_id = hashlib.md5(name.encode('utf-8')).hexdigest()      # 服务名称MD5后的服务id

        # 注册服务
        self._consul.agent.service.register(
            name,
            service_id,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            check=consul.Check().tcp(host, port, "5s", "30s", "30s"))

    def get_service(self, name):
        services = self._consul.agent.services()
        service = services.get(name)
        if not service:
            return None, None
        # addr = "{0}:{1}".format(service['Address'], service['Port'])
        return service['Address'], service['Port']
