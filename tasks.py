#!/usr/bin/env python
from pathlib import Path

from invoke import task

from deploy.docker_image import DockerImage
from deploy.helm_package import HelmPackage
from deploy.typescript_client import TypescriptClient


class ReleaseProject:
    project_name: str
    docker_project_name: str
    old_version: str
    new_version: str
    _node_client: TypescriptClient = None
    _helm_package: HelmPackage = None
    _docker_image: DockerImage = None

    def __init__(self, c, bump):
        self.c = c
        self.bump = bump
        self.project_name = "pymockserver"
        self.project_dir = Path(__file__).parent

    def run(self):
        self.bump_version()
        self.build_packages()
        self.publish_packages()

    def bump_version(self):
        self._fill_old_version()
        if self.bump:
            self._bump_version()
        self._fill_new_version()

    def build_packages(self):
        self.node_client.build()
        self.helm_package.build()
        self.docker_image.build()

    def publish_packages(self):
        self._push_version_to_git()
        self.docker_image.publish()
        self.node_client.publish()

    @property
    def docker_image(self):
        if self._docker_image is None:
            self._docker_image = DockerImage(new_version=self.new_version, project_name=self.project_name)
        return self._docker_image

    @property
    def helm_package(self):
        if self._helm_package is None:
            self._helm_package = HelmPackage(
                project_dir=self.project_dir, new_version=self.new_version, project_name=self.project_name
            )
        return self._helm_package

    @property
    def node_client(self):
        if self._node_client is None:
            self._node_client = TypescriptClient(project_dir=self.project_dir, new_version=self.new_version)
        return self._node_client

    def _push_version_to_git(self):
        self.__run("git push --follow-tags")

    def _bump_version(self):
        self.__run(f"cz bump -ch", warn=False)

    def _fill_new_version(self):
        self.new_version = self._get_project_version()

    def _fill_old_version(self):
        self.old_version = self._get_project_version()

    def _get_project_version(self):
        return self.__run('poetry version | cut -d" " -f2').strip()

    def __run(self, command, hide=True, warn=True):
        output = self.c.run(command, hide=hide, warn=warn, pty=True)
        return output.stdout


@task
def publish(c, bump=True):
    release = ReleaseProject(c, bump)
    release.run()
    print(f"Released new version: {release.new_version}")
