import docker

class DockerService(object):

    docker_client = None
    def __init__(self):
        self.docker_client = docker.from_env()

    def list(self, filters, status="running"):
        filters["status"] = status
        return self.docker_client.containers.list(filters=filters)
        #return [ c for c in self.docker_client.containers.list(filters=filters) if c.status == status ]
