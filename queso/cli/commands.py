import os
from typing import Tuple

import click

try:
    from uvicorn import main as uvicorn_command
except ImportError:
    uvicorn_command = None

from queso import scaffold
from queso.commands import CustomCommandsGroup, command, Command
from queso.versions import get_versions


class ServeCommand(Command):
    include_options_metavar = False

    def format_options(self, ctx, formatter):
        return click.Command.format_options(uvicorn_command, ctx, formatter)


@command(cls=ServeCommand)
@click.argument("app", required=False, default="app:app")
@click.argument("uvicorn_options", nargs=-1, type=click.UNPROCESSED)
def serve(app, uvicorn_options: Tuple[str]):
    """Start a uvicorn server for `app:app`.

    Use `APP` to customize the app location.
    
    uvicorn options must be separated with a `--` marker.
    """
    assert uvicorn_command is not None, "uvicorn must be installed"
    uvicorn_command.main([app, *uvicorn_options])


@command(name="init:custom")
@click.option(
    "-d", "--directory", default="", help="Where files should be generated."
)
def init_custom(directory: str):
    """Generate files required to build custom commands."""
    dest = os.path.join(directory, CustomCommandsGroup.path())
    scaffold.copy("queso.py", dest)
    click.echo(click.style(f"Generated {dest}", fg="green"))
    click.echo("Open the file and start building!")


@command()
def version():
    """Show version information and exit."""
    click.echo(str(get_versions()))

