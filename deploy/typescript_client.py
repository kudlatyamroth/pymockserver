import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from deploy.local_invoke import context, run
from deploy.log import section


@dataclass
class TypescriptClient:
    project_dir: Path
    client_dir: Path = Path(".")
    client: str = "typescript-node"

    def __post_init__(self):
        self.client_dir = self.project_dir.joinpath("clients").joinpath(self.client)

    def build(self):
        section(f"Start build {self.client} client")
        self._build_openapi()
        self._build_node_client()

    def _push_node_client(self):
        client = "typescript-node"
        client_dir = self.project_dir.joinpath("clients").joinpath(client)
        with context.cd(str(client_dir)):
            run(f"npm publish", msg="Publish npm package")

    def _build_node_client(self):
        docker_user_password = self.project_dir.joinpath(".docker_user_passwd")
        current_user = run("id -u", quite=True).strip()
        current_group = run("id -g", quite=True).strip()
        client = "typescript-node"
        client_dir = self.project_dir.joinpath("clients").joinpath(client)

        with open(str(docker_user_password), "w") as file:
            file.write(f"user:x:{current_user}:{current_group}:::/bin/bash")

        run(
            f"docker run --rm -u {current_user}:{current_group} -v '{self.project_dir}:/local' \
            openapitools/openapi-generator-cli:latest generate -g {client} \
            -i /local/openapi.json -o /local/clients/{client}/src \
            --additional-properties='supportsES6=true' --skip-validate-spec",
            msg=f"Generate {self.client}",
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

        with context.cd(str(client_dir)):
            run("npx tsc", msg=f"Build {self.client} client")
            run("npx prettier --write src/** dist/**/*.js > /dev/null", msg=f"Prettier {self.client} sources")

    def _build_openapi(self):
        import sys

        sys.path.append(str(self.project_dir.joinpath("src")))

        from main import app

        with open(str(self.project_dir.joinpath("openapi.json")), "w") as openapi_file:
            json.dump(app.openapi(), openapi_file, indent=2)
