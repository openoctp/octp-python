from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

from octp.core.builder import build_envelope
from octp.git.reader import read_repo
from octp.identity.keymanager import ensure_keypair
from octp.identity.resolver import resolve_developer_id
from octp.output.formatter import (
    print_envelope_summary,
    print_header,
    print_success,
    print_verification_results,
)
from octp.provenance.collector import collect_interactively
from octp.verification.registry import run_all

console = Console()


def get_default_provenance() -> dict:
    """Get default provenance data for non-interactive mode.

    For OCTP project: defaults to AI-assisted with substantial review.
    """
    return {
        "method": "ai_assisted_human_reviewed",
        "ai_tools": [
            {
                "model": "claude-sonnet-4-6",
                "vendor": "anthropic",
                "version": "20260226",
                "usage_type": "architecture_and_implementation",
            },
            {
                "model": "kimi-k2.5",
                "vendor": "moonshot",
                "version": "20260226",
                "usage_type": "implementation_and_scaffolding",
            },
        ],
        "human_review_level": "substantial_modification",
        "human_review_duration_minutes": None,
        "optional_context": {},
    }


def is_interactive() -> bool:
    """Check if running in an interactive terminal."""
    return sys.stdin.isatty() and sys.stdout.isatty()


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
    profile: str = typer.Option(
        "full",
        "--profile",
        "-p",
        help="Runner profile: fast (3-8s), full (all checks), ci, security",
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
    console.print(f"  Profile    : [cyan]{profile}[/cyan]")

    # Resolve identity
    ensure_keypair()
    developer_id = resolve_developer_id()
    console.print(f"  Developer  : [cyan]{developer_id}[/cyan]\n")

    # Run verification checks
    check_results = run_all(repo_info.root, profile=profile)
    print_verification_results(check_results)

    # Collect provenance declaration
    if yes:
        # Explicit --yes flag: use defaults
        provenance_data = get_default_provenance()
        console.print("\n[dim]Using default provenance (non-interactive mode)[/dim]")
    elif not is_interactive():
        # No TTY detected: use defaults with warning
        provenance_data = get_default_provenance()
        console.print(
            "\n[yellow]Warning:[/yellow] Non-interactive mode detected. "
            "Using default provenance. Use --yes to suppress this warning."
        )
    else:
        # Interactive: collect from user
        try:
            provenance_data = collect_interactively()
        except Exception as e:
            console.print(f"\n[red]Error collecting input:[/red] {e}")
            console.print("[dim]Falling back to default provenance...[/dim]")
            provenance_data = get_default_provenance()

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
