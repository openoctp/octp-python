from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from octp.core.envelope import OCTPEnvelope
from octp.integrity.hasher import hash_payload
from octp.output.formatter import print_header, print_verify_result

console = Console()


def verify_command(
    envelope_path: Path = typer.Argument(
        ..., help="Path to the envelope JSON file to verify"
    ),
):
    """Verify a trust envelope — check integrity and signature."""

    print_header()

    if not envelope_path.exists():
        console.print(f"[red]Error:[/red] Envelope file not found: {envelope_path}")
        raise typer.Exit(1)

    try:
        data = json.loads(envelope_path.read_text())
        envelope = OCTPEnvelope.model_validate(data)
    except Exception as e:
        print_verify_result(False, f"Could not parse envelope: {e}")
        raise typer.Exit(1)

    if not envelope.integrity:
        print_verify_result(False, "No integrity section found in envelope")
        raise typer.Exit(1)

    # Recompute payload hash
    payload_dict = envelope.to_signable_dict()
    computed_hash = hash_payload(payload_dict)

    if computed_hash != envelope.integrity.payload_hash:
        print_verify_result(
            False, "Payload hash mismatch — envelope has been tampered with"
        )
        raise typer.Exit(1)

    # Note: full signature verification requires public key lookup
    # In v0.1 we verify the hash integrity and flag if signature is present
    console.print(f"\n  Envelope   : [cyan]{envelope_path}[/cyan]")
    console.print(f"  Developer  : [cyan]{envelope.provenance.developer_id}[/cyan]")
    console.print(f"  Method     : [cyan]{envelope.provenance.method.value}[/cyan]")
    console.print(f"  Commit     : [cyan]{envelope.commit_hash[:12]}[/cyan]")

    print_verify_result(True)
    console.print(
        "\n[dim]Note: v0.1 verifies payload integrity. "
        "Full signature verification against public key registry coming in v0.2.[/dim]"
    )
