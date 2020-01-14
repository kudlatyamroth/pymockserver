from dataclasses import dataclass

from deploy import log
from deploy.local_invoke import run


@dataclass
class DockerImage:
    new_version: str
    project_name: str

    def __post_init__(self):
        self.image_name = f"kudlatyamroth/{self.project_name}"

    def build(self):
        log.section(f"Start build docker image: {self.image_name}:{self.new_version}")
        run(f"docker build -t {self.image_name}:{self.new_version} .")
        run(f"docker build -t {self.image_name}:latest .")

    def publish(self):
        log.section(f"Publishing docker image: {self.image_name}:{self.new_version}")
        run(f"docker push {self.image_name}:{self.new_version}")
        run(f"docker push {self.image_name}:latest")
