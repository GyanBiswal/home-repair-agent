from typing import Literal

from pydantic import BaseModel, Field


class QuickDiagnosis(BaseModel):
    """A first, simple structured answer. We'll build the full version in Phase 6."""

    appliance: str = Field(description="The appliance mentioned, e.g. 'washing machine'")
    likely_issue: str = Field(description="The single most likely cause, in one sentence")
    safe_steps: list[str] = Field(description="2-4 simple steps a homeowner can safely try")
    call_technician: bool = Field(description="True if this needs a professional")
    confidence: Literal["low", "medium", "high"]