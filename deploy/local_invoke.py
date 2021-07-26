from typing import Optional

from invoke import Context

from deploy.log import status

context = Context()


class OutputDef:
    stdout: str = ""

    def __init__(self) -> None:
        self.failed = False


def run(command: str, hide: bool = True, warn: bool = True, msg: str = "", quite: bool = False) -> Optional[str]:
    output = OutputDef()
    try:
        output = context.run(command, hide=hide, warn=warn, pty=True)
        return output.stdout
    finally:
        if not quite:
            status(msg, output.failed)
