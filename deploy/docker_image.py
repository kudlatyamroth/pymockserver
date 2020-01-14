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
        log.section(f"Build docker images")
        run(
            f"docker build -t {self.image_name}:{self.new_version} .",
            msg=f"version: {self.image_name}:{self.new_version}",
        )
        run(f"docker build -t {self.image_name}:latest .", msg=f"version: {self.image_name}:latest")

    def publish(self):
        log.section(f"Publish docker images")
        run(f"docker push {self.image_name}:{self.new_version}", msg=f"version: {self.image_name}:{self.new_version}")
        run(f"docker push {self.image_name}:latest", msg=f"version: {self.image_name}:latest")
