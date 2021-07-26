from dataclasses import dataclass
from pathlib import Path

from deploy import log
from deploy.local_invoke import context, run


@dataclass
class HelmPackage:
    project_dir: Path
    new_version: str
    project_name: str

    def __post_init__(self) -> None:
        self.helm_v2_dir = self.project_dir.joinpath("helm_v2")
        self.helm_v3_dir = self.project_dir.joinpath("helm_v3")
        self.build_name = f"{self.project_name}-{self.new_version}.tgz"
        self._build_helm_v2_package_name = self.helm_v2_dir.joinpath(self.build_name)
        self._build_helm_v3_package_name = self.helm_v3_dir.joinpath(self.build_name)
        self._helm_v2_package = self.helm_v2_dir.joinpath(f"helm_v2-{self.build_name}")
        self._helm_v3_package = self.helm_v3_dir.joinpath(f"helm_v3-{self.build_name}")

    def build(self) -> None:
        log.section("Build helm packages")
        self._build_helm_v2_package()
        self._build_helm_v3_package()

    def _build_helm_v2_package(self) -> None:
        with context.cd(str(self.helm_v2_dir)):
            run(f"helm package {self.project_name}", msg="Build helm v2 package")
        self._build_helm_v2_package_name.rename(self._helm_v2_package)

    def _build_helm_v3_package(self) -> None:
        with context.cd(str(self.helm_v3_dir)):
            run(f"helm3 package {self.project_name}", msg="Build helm v3 package")
        self._build_helm_v3_package_name.rename(self._helm_v3_package)
