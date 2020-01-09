#!/usr/bin/env python
import json
import shutil
from pathlib import Path

from invoke import task


class ReleaseProject:
    project_name: str
    docker_project_name: str
    old_version: str
    new_version: str

    def __init__(self, c, part, bump):
        self.c = c
        self.part = part
        self.bump = bump
        self.project_name = "pymockserver"
        self.docker_project_name = f"kudlatyamroth/{self.project_name}"
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
        self._build_openapi()
        self._build_node_client()
        self._build_helm_packages()
        self._build_docker_images()

    def publish_packages(self):
        # self._push_version_to_git()
        # self._push_docker_images()
        pass

    def _build_node_client(self):
        docker_user_password = self.project_dir.joinpath(".docker_user_passwd")
        current_user = self.__run("id -u").strip()
        current_group = self.__run("id -g").strip()
        client = "typescript-node"
        client_dir = self.project_dir.joinpath("clients").joinpath(client)

        with open(docker_user_password, "w") as file:
            file.write(f"user:x:{current_user}:{current_group}:::/bin/bash")

        self.__run(
            f"docker run --rm -u {current_user}:{current_group} -v '{self.project_dir}:/local' \
            openapitools/openapi-generator-cli:latest generate -g {client} \
            -i /local/openapi.json -o /local/clients/{client}/src \
            --additional-properties='supportsES6=true' --skip-validate-spec"
        )

        files_to_delete = (
            docker_user_password,
            client_dir.joinpath("src/.gitignore"),
            client_dir.joinpath("src/git_push.sh"),
            client_dir.joinpath("src/.openapi-generator"),
            client_dir.joinpath("src/.openapi-generator-ignore"),
        )

        for file in files_to_delete:
            file.unlink() if file.is_file() else shutil.rmtree(file)

        with self.c.cd(str(client_dir)):
            self.__run("npx tsc")
            self.__run("npx prettier --write src/** dist/**/*.js > /dev/null")

    def _build_openapi(self):
        import sys

        sys.path.append(str(self.project_dir.joinpath("src")))

        from main import app

        with open("openapi.json", "w") as openapi_file:
            json.dump(app.openapi(), openapi_file, indent=2)

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
def publish(c, version="minor", bump=True):
    release = ReleaseProject(c, version, bump)
    release.run()
    print(f"Released new version: {release.new_version}")
