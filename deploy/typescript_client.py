import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from git import Repo

from deploy.local_invoke import context, run
from deploy import log


@dataclass
class TypescriptClient:
    project_dir: Path
    new_version: str
    client: str = "typescript-node"

    def __post_init__(self):
        self.client_dir = self.project_dir.joinpath("clients").joinpath(self.client)
        self.docker_credentials_file = self.project_dir.joinpath(".docker_user_passwd")
        self.user = run("id -u", quite=True).strip()
        self.group = run("id -g", quite=True).strip()
        self.repo = Repo(self.project_dir)

    def build(self):
        log.section(f"Start build {self.client} client")
        self._build_openapi()
        self._write_credentials_to_file()
        self._generate_node_client()
        self._clean_generated_files()
        self._build_node_client()
        self._commit_generated_client()

    def publish(self):
        with context.cd(str(self.client_dir)):
            run(f"npm publish", msg="Publish npm package")

    def _commit_generated_client(self):
        if not self.repo.is_dirty():
            log.debug("Nothing to commit")
            return

        try:
            log.info("Adding files for commit")
            self.repo.git.add(".")
            self.repo.index.commit(f"generated typescript client version: {self.new_version}")
            log.status("Adding commit with generated client")
        except Exception as e:
            log.status("Adding commit with generated client", failed=True)
            raise Exception from e

    def _build_node_client(self):
        with context.cd(str(self.client_dir)):
            run("npx tsc", msg=f"Build {self.client} client")
            run("npx prettier --write src/** dist/**/*.js > /dev/null", msg=f"Prettier {self.client} sources")

    def _clean_generated_files(self):
        log.info("Clean obsolete files")
        files_to_delete = (
            self.docker_credentials_file,
            self.client_dir.joinpath("src/.gitignore"),
            self.client_dir.joinpath("src/git_push.sh"),
            self.client_dir.joinpath("src/.openapi-generator"),
            self.client_dir.joinpath("src/.openapi-generator-ignore"),
        )

        for file in files_to_delete:
            file.unlink() if file.is_file() else shutil.rmtree(file)

    def _generate_node_client(self):
        run(
            f"docker run --rm -u {self.user}:{self.group} -v '{self.project_dir}:/local' \
            openapitools/openapi-generator-cli:latest generate -g {self.client} \
            -i /local/openapi.json -o /local/clients/{self.client}/src \
            --additional-properties='supportsES6=true' --skip-validate-spec",
            msg=f"Generate {self.client}",
        )

    def _write_credentials_to_file(self):
        log.info("Save docker credentials")
        with open(str(self.docker_credentials_file), "w") as file:
            file.write(f"user:x:{self.user}:{self.group}:::/bin/bash")

    def _build_openapi(self):
        log.info("Save openApi file")
        import sys

        sys.path.append(str(self.project_dir.joinpath("pymockserver")))

        from main import app

        with open(str(self.project_dir.joinpath("openapi.json")), "w") as openapi_file:
            json.dump(app.openapi(), openapi_file, indent=2)
