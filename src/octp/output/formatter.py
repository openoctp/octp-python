from __future__ import annotations
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from octp.core.envelope import OCTPEnvelope, AnalysisResult

console = Console()


def print_header():
    console.print(
        Panel(
            "[bold blue]OCTP[/bold blue] — Open Contribution Trust Protocol v0.1",
            box=box.ROUNDED,
        )
    )


def print_verification_results(results: dict):
    console.print("\n[bold]Running verification checks...[/bold]")
    for name, result in results.items():
        icon = "✓" if result.passed else "✗"
        colour = "green" if result.passed else "red"
        console.print(
            f"  [{colour}]{icon}[/{colour}] {result.tool_name} — {result.detail}"
        )


def print_envelope_summary(envelope: OCTPEnvelope):
    console.print("\n[bold blue]Trust Envelope Summary[/bold blue]")
    console.print("─" * 50)

    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column()

    table.add_row("Repository", envelope.repository)
    table.add_row("Commit", envelope.commit_hash[:12] + "...")
    table.add_row("Developer", envelope.provenance.developer_id)
    table.add_row("Method", envelope.provenance.method.value)
    table.add_row("Review level", envelope.provenance.human_review_level.value)

    v = envelope.verification
    tests = "✓ passed" if v.tests_passed else "✗ failed"
    analysis = v.static_analysis.value
    deps = v.dependency_check.value
    table.add_row("Tests", tests)
    table.add_row("Static analysis", analysis)
    table.add_row("Dependencies", deps)

    if envelope.optional_context:
        ctx = envelope.optional_context
        if ctx.self_assessed_confidence:
            table.add_row("Confidence", ctx.self_assessed_confidence.value)
        if ctx.areas_of_uncertainty:
            table.add_row("Uncertainty", ctx.areas_of_uncertainty)
        if ctx.issue_reference:
            table.add_row("Issue", ctx.issue_reference)

    console.print(table)


def print_success(envelope_path: str):
    console.print(
        f"\n[bold green]✓ Envelope signed and written to {envelope_path}[/bold green]"
    )


def print_verify_result(valid: bool, reason: str = ""):
    if valid:
        console.print(
            "\n[bold green]✓ Envelope is valid — signature verified[/bold green]"
        )
    else:
        console.print(f"\n[bold red]✗ Envelope is INVALID — {reason}[/bold red]")
