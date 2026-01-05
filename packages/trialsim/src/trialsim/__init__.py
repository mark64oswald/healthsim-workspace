"""TrialSim - Synthetic Clinical Trial Data Generation.

This package generates synthetic clinical trial data including:
- Trial subjects with demographics and eligibility
- Protocol visits (scheduled and unscheduled)
- Adverse events with CTCAE grading
- Drug exposure records
- Laboratory results
- Efficacy assessments

Exports to CDISC/SDTM formats.
"""

from trialsim.core.generator import (
    AdverseEventGenerator,
    ExposureGenerator,
    TrialSubjectGenerator,
    VisitGenerator,
)
from trialsim.core.models import (
    AdverseEvent,
    Exposure,
    Protocol,
    Site,
    Subject,
    Visit,
)

__version__ = "1.0.0"

__all__ = [
    # Generators
    "TrialSubjectGenerator",
    "VisitGenerator",
    "AdverseEventGenerator",
    "ExposureGenerator",
    # Models
    "Subject",
    "Site",
    "Protocol",
    "Visit",
    "AdverseEvent",
    "Exposure",
]
