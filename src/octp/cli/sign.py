from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from octp.git.reader import read_repo
from octp.identity.resolver import resolve_developer_id
from octp.identity.keymanager import ensure_keypair
from octp.verification.registry import run_all
from octp.provenance.collector import collect_interactively
from octp.core.builder import build_envelope
from octp.output.formatter import (
    print_header,
    print_verification_results,
    print_envelope_summary,
    print_success,
)
import json

console = Console()


def sign_command(
    output: Path = typer.Option(
        Path(".octp-envelope.json"),
        "--output",
        "-o",
        help="Path to write the envelope JSON",
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Skip interactive prompts — use defaults"
    ),
):
    """Generate and sign a trust envelope for the current commit."""

    print_header()

    # Read git state
    try:
        repo_info = read_repo()
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    console.print(f"\n  Repository : [cyan]{repo_info.repository}[/cyan]")
    console.print(f"  Commit     : [cyan]{repo_info.commit_hash[:12]}[/cyan]")

    # Resolve identity
    ensure_keypair()
    developer_id = resolve_developer_id()
    console.print(f"  Developer  : [cyan]{developer_id}[/cyan]\n")

    # Run verification checks
    check_results = run_all(repo_info.root)
    print_verification_results(check_results)

    # Collect provenance declaration
    if yes:
        provenance_data = {
            "method": "human_only",
            "human_review_level": "moderate_review",
            "optional_context": {},
        }
    else:
        provenance_data = collect_interactively()

    # Build and sign envelope
    envelope = build_envelope(
        repo_info=repo_info,
        developer_id=developer_id,
        provenance_data=provenance_data,
        check_results=check_results,
    )

    # Write envelope
    envelope_json = envelope.model_dump_json(indent=2)
    output.write_text(envelope_json)

    # Print summary
    print_envelope_summary(envelope)
    print_success(str(output))
