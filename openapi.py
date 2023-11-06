#!/usr/bin/env python
import json
import sys
from pathlib import Path

project_dir = Path(__file__).parent


def generate_openapi():
    from main import app

    with open(str(project_dir.joinpath("openapi.json")), "w") as openapi_file:
        json.dump(app.openapi(), openapi_file, indent=2)


print("Save openApi file")

sys.path.append(str(project_dir.joinpath("pymockserver")))

generate_openapi()

print("Generated new openapi")
