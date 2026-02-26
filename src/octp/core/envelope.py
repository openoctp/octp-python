from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ProvenanceMethod(str, Enum):
    HUMAN_ONLY = "human_only"
    AI_ASSISTED_HUMAN_REVIEWED = "ai_assisted_human_reviewed"
    AI_GENERATED_HUMAN_REVIEWED = "ai_generated_human_reviewed"
    AI_GENERATED_UNREVIEWED = "ai_generated_unreviewed"


class ReviewLevel(str, Enum):
    NONE = "none"
    GLANCE = "glance"
    MODERATE = "moderate_review"
    SUBSTANTIAL = "substantial_modification"
    REWRITE = "complete_rewrite"


class AnalysisResult(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AITool(BaseModel):
    model: str
    vendor: str
    version: str
    usage_type: str


class Provenance(BaseModel):
    method: ProvenanceMethod
    ai_tools: Optional[list[AITool]] = None
    human_review_level: ReviewLevel
    human_review_duration_minutes: Optional[int] = Field(None, ge=0)
    developer_id: str


class Verification(BaseModel):
    tests_passed: bool
    test_suite_hash: Optional[str] = None
    static_analysis: AnalysisResult
    static_analysis_tool: Optional[str] = None
    dependency_check: AnalysisResult
    novel_dependencies_introduced: bool


class Integrity(BaseModel):
    payload_hash: str
    developer_signature: str
    signature_algorithm: str = "ES256"
    signed_at: datetime


class OptionalContext(BaseModel):
    issue_reference: Optional[str] = None
    self_assessed_confidence: Optional[Confidence] = None
    areas_of_uncertainty: Optional[str] = None
    time_in_codebase_minutes: Optional[int] = Field(None, ge=0)


class OCTPEnvelope(BaseModel):
    octp_version: str = "0.1"
    contribution_id: str
    timestamp: datetime
    repository: str
    commit_hash: str
    provenance: Provenance
    verification: Verification
    integrity: Optional[Integrity] = None
    optional_context: Optional[OptionalContext] = None

    def to_signable_dict(self) -> dict:
        """Returns envelope as dict excluding the integrity section.
        This is what gets hashed before signing."""
        d = self.model_dump(mode="json", exclude={"integrity"})
        return d
