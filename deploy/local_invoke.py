from invoke import Context

from deploy.log import status

context = Context()


class OutputDef:
    def __init__(self):
        self.failed = False


def run(command, hide=True, warn=True, msg="", quite=False):
    output = OutputDef()
    try:
        output = context.run(command, hide=hide, warn=warn, pty=True)
        return output.stdout
    finally:
        if not quite:
            status(msg, output.failed)
