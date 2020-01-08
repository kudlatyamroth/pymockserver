#!/usr/bin/env python
from invoke import task


class ReleaseProject:
    project_name: str
    docker_project_name: str
    old_version: str
    new_version: str

    def __init__(self, c, part):
        self.c = c
        self.part = part
        self.project_name = "pymockserver"
        self.docker_project_name = f"kudlatyamroth/{self.project_name}"

    def run(self):
        self._fill_old_version()
        self._bump_version()
        self._fill_new_version()

        self._build_helm_packages()
        self._build_docker_images()

        self._push_version_to_git()
        self._push_docker_images()

    def _push_docker_images(self):
        self.__run(f"docker push {self.docker_project_name}:{self.new_version}")
        self.__run(f"docker push {self.docker_project_name}:latest")

    def _build_docker_images(self):
        self.__run(f"docker build -t {self.docker_project_name}:{self.new_version} .")
        self.__run(f"docker build -t {self.docker_project_name}:latest .")

    def _push_version_to_git(self):
        self.__run("git push --follow-tags")

    def _build_helm_packages(self):
        with self.c.cd("helm_v3"):
            self.__run(f"helm3 package {self.project_name}")
        with self.c.cd("helm_v2"):
            self.__run(f"helm3 package {self.project_name}")

    def _bump_version(self):
        self.__run(f"bump2version -n {self.part}", warn=False)

    def _fill_new_version(self):
        self.new_version = self._get_project_version()

    def _fill_old_version(self):
        self.old_version = self._get_project_version()

    def _get_project_version(self):
        return self.__run('poetry version | cut -d" " -f2')

    def __run(self, command, hide=True, warn=True):
        output = self.c.run(command, hide=hide, warn=warn)
        return output.stdout


@task
def publish(c, version="minor"):
    release = ReleaseProject(c, version)
    release.run()
    print(f"Released new version: {release.new_version}")
