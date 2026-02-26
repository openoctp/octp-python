from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

DEFAULT_CONFIG = """\
[policy]
require_envelope = true
minimum_review_level = "moderate_review"
block_on_failed_tests = true
allow_unreviewed_ai = false

[runners]
test_runner = "pytest"
static_analysis = "semgrep"
dependency_check = "pip-audit"

[identity]
require_signed_envelope = true
key_registry = "github"
"""


def init_command(
    path: Path = typer.Argument(
        Path("."), help="Repository path to initialise OCTP in"
    ),
):
    """Initialise OCTP in a repository — creates .octp.toml"""

    config_path = path / ".octp.toml"

    if config_path.exists():
        overwrite = Confirm.ask(
            f".octp.toml already exists at {config_path}. Overwrite?"
        )
        if not overwrite:
            console.print("Aborted.")
            raise typer.Exit(0)

    config_path.write_text(DEFAULT_CONFIG)
    console.print(f"\n[green]✓[/green] Created {config_path}")
    console.print("\nNext steps:")
    console.print("  1. Review and adjust .octp.toml for your project")
    console.print("  2. Run [cyan]octp sign[/cyan] before submitting a pull request")
    console.print(
        "  3. Add to your CONTRIBUTING.md that contributors should run octp sign"
    )
    console.print("\nSpec: https://github.com/openoctp/spec")
