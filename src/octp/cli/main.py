import typer
from typing import Optional

app = typer.Typer(
    name="octp",
    help="Open Contribution Trust Protocol — generate and verify trust envelopes",
    add_completion=False,
)

from octp.cli.sign import sign_command
from octp.cli.verify import verify_command
from octp.cli.init import init_command

app.command(name="sign")(sign_command)
app.command(name="verify")(verify_command)
app.command(name="init")(init_command)


if __name__ == "__main__":
    app()
