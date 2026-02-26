from __future__ import annotations
from typing import Optional
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .models import ProvenanceMethod, ReviewLevel, AITool, Confidence

console = Console()


def collect_interactively() -> dict:
    """Collect provenance declaration interactively from the developer."""

    console.print("\n[bold blue]Provenance Declaration[/bold blue]")
    console.print("─" * 40)

    # Method
    console.print("\nHow was this contribution created?\n")
    methods = [
        ("1", "Human only", ProvenanceMethod.HUMAN_ONLY),
        (
            "2",
            "AI assisted, human reviewed",
            ProvenanceMethod.AI_ASSISTED_HUMAN_REVIEWED,
        ),
        (
            "3",
            "AI generated, human reviewed",
            ProvenanceMethod.AI_GENERATED_HUMAN_REVIEWED,
        ),
        ("4", "AI generated, unreviewed", ProvenanceMethod.AI_GENERATED_UNREVIEWED),
    ]
    for num, label, _ in methods:
        console.print(f"  [{num}] {label}")

    method_choice = Prompt.ask("\n", choices=["1", "2", "3", "4"], default="1")
    method = methods[int(method_choice) - 1][2]

    # AI tools (if applicable)
    ai_tools = []
    if method != ProvenanceMethod.HUMAN_ONLY:
        console.print(
            "\nWhich AI tools did you use? (comma separated, or press enter to skip)"
        )
        tools_input = Prompt.ask("", default="")
        if tools_input.strip():
            for tool_name in [t.strip() for t in tools_input.split(",")]:
                if tool_name:
                    ai_tools.append(
                        AITool(
                            model=tool_name,
                            vendor="unknown",
                            version="unknown",
                            usage_type="general",
                        )
                    )

    # Review level
    console.print("\nWhat was your level of review?\n")
    levels = [
        ("1", "Glance — brief look", ReviewLevel.GLANCE),
        ("2", "Moderate review — read and understood", ReviewLevel.MODERATE),
        (
            "3",
            "Substantial modification — significantly changed",
            ReviewLevel.SUBSTANTIAL,
        ),
        ("4", "Complete rewrite — AI used as reference only", ReviewLevel.REWRITE),
        ("5", "None", ReviewLevel.NONE),
    ]
    for num, label, _ in levels:
        console.print(f"  [{num}] {label}")

    level_choice = Prompt.ask("\n", choices=["1", "2", "3", "4", "5"], default="2")
    review_level = levels[int(level_choice) - 1][2]

    # Duration (optional)
    duration_str = Prompt.ask(
        "\nHow many minutes did you spend on this? (optional, press enter to skip)",
        default="",
    )
    duration = int(duration_str) if duration_str.strip().isdigit() else None

    # Optional context
    console.print("\n[bold blue]Optional Context[/bold blue]")
    console.print("─" * 40)

    issue_ref = Prompt.ask("\nIssue reference (e.g. #123, optional)", default="")

    confidence_input = Prompt.ask(
        "\nSelf-assessed confidence",
        choices=["low", "medium", "high"],
        default="medium",
    )

    uncertainty = Prompt.ask(
        "\nAny areas of uncertainty for the reviewer? (optional)", default=""
    )

    time_in_codebase_str = Prompt.ask(
        "\nMinutes spent reading the codebase before contributing? (optional)",
        default="",
    )
    time_in_codebase = (
        int(time_in_codebase_str) if time_in_codebase_str.strip().isdigit() else None
    )

    return {
        "method": method,
        "ai_tools": ai_tools if ai_tools else None,
        "human_review_level": review_level,
        "human_review_duration_minutes": duration,
        "optional_context": {
            "issue_reference": issue_ref.strip() or None,
            "self_assessed_confidence": confidence_input,
            "areas_of_uncertainty": uncertainty.strip() or None,
            "time_in_codebase_minutes": time_in_codebase,
        },
    }
