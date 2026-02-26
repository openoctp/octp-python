from __future__ import annotations

import uuid
from datetime import datetime, timezone

from octp.core.envelope import (
    AnalysisResult,
    Integrity,
    OCTPEnvelope,
    OptionalContext,
    Provenance,
    Verification,
)
from octp.git.reader import RepoInfo
from octp.identity.keymanager import sign_payload
from octp.integrity.hasher import hash_payload
from octp.verification.base import CheckResult


def build_envelope(
    repo_info: RepoInfo,
    developer_id: str,
    provenance_data: dict,
    check_results: dict[str, CheckResult],
) -> OCTPEnvelope:
    """Assemble a complete signed OCTPEnvelope."""

    # Build provenance
    ai_tools = provenance_data.get("ai_tools")
    provenance = Provenance(
        method=provenance_data["method"],
        ai_tools=ai_tools,
        human_review_level=provenance_data["human_review_level"],
        human_review_duration_minutes=provenance_data.get(
            "human_review_duration_minutes"
        ),
        developer_id=developer_id,
    )

    # Build verification from check results
    tests_result = check_results.get("pytest")
    static_result = check_results.get("semgrep") or check_results.get("bandit")
    deps_result = check_results.get("pip-audit")

    verification = Verification(
        tests_passed=tests_result.passed if tests_result else False,
        test_suite_hash=tests_result.suite_hash if tests_result else None,
        static_analysis=AnalysisResult(
            "passed"
            if static_result and static_result.passed
            else "failed"
            if static_result and not static_result.passed
            else "skipped"
        ),
        static_analysis_tool=static_result.tool_name if static_result else None,
        dependency_check=AnalysisResult(
            "passed"
            if deps_result and deps_result.passed
            else "failed"
            if deps_result and not deps_result.passed
            else "skipped"
        ),
        novel_dependencies_introduced=False,  # v0.1: always false, future runner
    )

    # Build optional context
    ctx_data = provenance_data.get("optional_context", {})
    optional_context = (
        OptionalContext(
            issue_reference=ctx_data.get("issue_reference"),
            self_assessed_confidence=ctx_data.get("self_assessed_confidence"),
            areas_of_uncertainty=ctx_data.get("areas_of_uncertainty"),
            time_in_codebase_minutes=ctx_data.get("time_in_codebase_minutes"),
        )
        if ctx_data
        else None
    )

    # Build unsigned envelope
    envelope = OCTPEnvelope(
        octp_version="0.1",
        contribution_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
        repository=repo_info.repository,
        commit_hash=repo_info.commit_hash,
        provenance=provenance,
        verification=verification,
        optional_context=optional_context,
    )

    # Hash and sign
    payload_dict = envelope.to_signable_dict()
    payload_hash = hash_payload(payload_dict)
    signature = sign_payload(payload_hash)

    envelope.integrity = Integrity(
        payload_hash=payload_hash,
        developer_signature=signature,
        signature_algorithm="ES256",
        signed_at=datetime.now(timezone.utc),
    )

    return envelope
