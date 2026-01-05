"""Shared journey engine for cross-product event orchestration.

This module provides the core journey execution engine that can be used
across all HealthSim products (PatientSim, MemberSim, RxMemberSim, etc.).

The journey engine follows a timeline-based approach:
1. JourneySpecification defines the event sequence
2. JourneyEngine creates timelines with scheduled events
3. Product-specific handlers execute events
4. Cross-product triggers coordinate related events
"""

from __future__ import annotations

import hashlib
import random
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, Field


# =============================================================================
# Event Type System
# =============================================================================

class BaseEventType(str, Enum):
    """Base event types common across products."""
    
    # Lifecycle events
    ENTITY_CREATED = "entity_created"
    ENTITY_UPDATED = "entity_updated"
    ENTITY_TERMINATED = "entity_terminated"
    
    # Temporal markers
    JOURNEY_START = "journey_start"
    JOURNEY_END = "journey_end"
    MILESTONE = "milestone"
    
    # Cross-product triggers
    TRIGGER_OUTBOUND = "trigger_outbound"
    TRIGGER_RECEIVED = "trigger_received"


class PatientEventType(str, Enum):
    """PatientSim-specific event types."""
    
    # ADT events
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    TRANSFER = "transfer"
    
    # Clinical events
    ENCOUNTER = "encounter"
    OBSERVATION = "observation"
    PROCEDURE = "procedure"
    MEDICATION_ORDER = "medication_order"
    LAB_ORDER = "lab_order"
    LAB_RESULT = "lab_result"
    DIAGNOSIS = "diagnosis"
    
    # Care coordination
    REFERRAL = "referral"
    CARE_PLAN_UPDATE = "care_plan_update"


class MemberEventType(str, Enum):
    """MemberSim-specific event types."""
    
    # Enrollment
    NEW_ENROLLMENT = "new_enrollment"
    TERMINATION = "termination"
    PLAN_CHANGE = "plan_change"
    
    # Claims
    CLAIM_PROFESSIONAL = "claim_professional"
    CLAIM_INSTITUTIONAL = "claim_institutional"
    CLAIM_PHARMACY = "claim_pharmacy"
    
    # Quality
    GAP_IDENTIFIED = "gap_identified"
    GAP_CLOSED = "gap_closed"


class RxEventType(str, Enum):
    """RxMemberSim-specific event types."""
    
    # Prescription lifecycle
    NEW_RX = "new_rx"
    REFILL = "refill"
    FILL = "fill"
    REVERSAL = "reversal"
    
    # Therapy management
    THERAPY_START = "therapy_start"
    THERAPY_CHANGE = "therapy_change"
    THERAPY_DISCONTINUE = "therapy_discontinue"
    
    # Adherence
    ADHERENCE_GAP = "adherence_gap"
    MPR_THRESHOLD = "mpr_threshold"


class TrialEventType(str, Enum):
    """TrialSim-specific event types."""
    
    # Enrollment
    SCREENING = "screening"
    RANDOMIZATION = "randomization"
    WITHDRAWAL = "withdrawal"
    
    # Visits
    SCHEDULED_VISIT = "scheduled_visit"
    UNSCHEDULED_VISIT = "unscheduled_visit"
    
    # Safety
    ADVERSE_EVENT = "adverse_event"
    SERIOUS_ADVERSE_EVENT = "serious_adverse_event"
    
    # Protocol
    PROTOCOL_DEVIATION = "protocol_deviation"
    DOSE_MODIFICATION = "dose_modification"



# =============================================================================
# Delay and Timing Specifications
# =============================================================================

class DelaySpec(BaseModel):
    """Specification for event delay/timing."""
    
    days: int = 0
    days_min: int | None = None
    days_max: int | None = None
    distribution: str = "fixed"  # fixed, uniform, normal
    
    def to_timedelta(self, seed: int | None = None) -> timedelta:
        """Convert to actual timedelta, applying randomization if needed."""
        rng = random.Random(seed) if seed else random.Random()
        
        if self.distribution == "fixed":
            return timedelta(days=self.days)
        
        elif self.distribution == "uniform":
            min_days = self.days_min if self.days_min is not None else self.days
            max_days = self.days_max if self.days_max is not None else self.days
            actual_days = rng.randint(min_days, max_days)
            return timedelta(days=actual_days)
        
        elif self.distribution == "normal":
            # Use days as mean, (max-min)/4 as std_dev
            mean = self.days
            std_dev = (self.days_max - self.days_min) / 4 if self.days_min and self.days_max else 2
            actual_days = max(0, int(rng.gauss(mean, std_dev)))
            return timedelta(days=actual_days)
        
        return timedelta(days=self.days)


# =============================================================================
# Condition System
# =============================================================================

class EventCondition(BaseModel):
    """Condition that must be met for an event to occur."""
    
    field: str  # Path to context field (e.g., "demographics.age")
    operator: str  # eq, ne, gt, gte, lt, lte, in, not_in, contains
    value: Any
    
    def evaluate(self, context: dict[str, Any]) -> bool:
        """Evaluate condition against context."""
        # Navigate to field value
        actual = self._get_field_value(context, self.field)
        if actual is None:
            return False
        
        # Apply operator
        if self.operator == "eq":
            return actual == self.value
        elif self.operator == "ne":
            return actual != self.value
        elif self.operator == "gt":
            return actual > self.value
        elif self.operator == "gte":
            return actual >= self.value
        elif self.operator == "lt":
            return actual < self.value
        elif self.operator == "lte":
            return actual <= self.value
        elif self.operator == "in":
            return actual in self.value
        elif self.operator == "not_in":
            return actual not in self.value
        elif self.operator == "contains":
            return self.value in actual
        
        return False
    
    def _get_field_value(self, context: dict, path: str) -> Any:
        """Navigate to nested field value."""
        parts = path.split(".")
        current = context
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current


# =============================================================================
# Event Definitions
# =============================================================================

class EventDefinition(BaseModel):
    """Definition of an event within a journey."""
    
    event_id: str
    name: str
    event_type: str  # String to support any event type enum
    product: str = "core"  # Which product owns this event
    
    # Timing
    delay: DelaySpec = Field(default_factory=DelaySpec)
    depends_on: str | None = None  # event_id of dependency
    
    # Conditions
    conditions: list[EventCondition] = Field(default_factory=list)
    
    # Probability (for optional events)
    probability: float = 1.0
    
    # Event-specific parameters
    parameters: dict[str, Any] = Field(default_factory=dict)
    
    # Cross-product triggers
    triggers: list["TriggerSpec"] = Field(default_factory=list)


class TriggerSpec(BaseModel):
    """Specification for a cross-product trigger."""
    
    target_product: str  # e.g., "membersim", "patientsim"
    event_type: str
    delay: DelaySpec = Field(default_factory=DelaySpec)
    parameters: dict[str, Any] = Field(default_factory=dict)
    condition: EventCondition | None = None



# =============================================================================
# Journey Specification
# =============================================================================

class JourneySpecification(BaseModel):
    """Complete specification for a journey (temporal event sequence)."""
    
    journey_id: str
    name: str
    description: str = ""
    version: str = "1.0"
    
    # Target products
    products: list[str] = Field(default_factory=lambda: ["patientsim"])
    
    # Duration
    duration_days: int | None = None
    
    # Events in the journey
    events: list[EventDefinition] = Field(default_factory=list)
    
    # Journey-level parameters
    parameters: dict[str, Any] = Field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: dict) -> "JourneySpecification":
        """Create from dictionary."""
        return cls(**data)


# =============================================================================
# Timeline Classes
# =============================================================================

@dataclass
class TimelineEvent:
    """A scheduled event on a timeline."""
    
    timeline_event_id: str
    journey_id: str
    event_definition_id: str
    scheduled_date: date
    event_type: str
    event_name: str
    product: str = "core"
    
    # Execution state
    status: str = "pending"  # pending, executed, skipped, failed
    executed_at: datetime | None = None
    result: dict[str, Any] = field(default_factory=dict)
    
    # Cross-product tracking
    triggered_events: list[str] = field(default_factory=list)


@dataclass 
class Timeline:
    """Timeline of events for an entity."""
    
    entity_id: str
    entity_type: str  # "patient", "member", "rx_member", etc.
    journey_ids: list[str] = field(default_factory=list)
    start_date: date = field(default_factory=date.today)
    end_date: date | None = None
    
    events: list[TimelineEvent] = field(default_factory=list)
    
    # Cross-product correlation
    linked_timelines: dict[str, str] = field(default_factory=dict)  # product -> timeline_id
    
    def add_event(self, event: TimelineEvent) -> None:
        """Add event to timeline, maintaining chronological order."""
        self.events.append(event)
        self.events.sort(key=lambda e: e.scheduled_date)
    
    def get_pending_events(self) -> list[TimelineEvent]:
        """Get all pending events in chronological order."""
        return [e for e in self.events if e.status == "pending"]
    
    def get_events_by_date(self, target_date: date) -> list[TimelineEvent]:
        """Get events scheduled for a specific date."""
        return [e for e in self.events if e.scheduled_date == target_date]
    
    def get_events_up_to(self, target_date: date) -> list[TimelineEvent]:
        """Get pending events up to and including target date."""
        return [
            e for e in self.events 
            if e.status == "pending" and e.scheduled_date <= target_date
        ]
    
    def mark_executed(self, event_id: str, result: dict[str, Any]) -> None:
        """Mark an event as executed with result."""
        for event in self.events:
            if event.timeline_event_id == event_id:
                event.status = "executed"
                event.executed_at = datetime.utcnow()
                event.result = result
                break


# =============================================================================
# Event Handler Protocol
# =============================================================================

class EventHandler(Protocol):
    """Protocol for event handlers."""
    
    def __call__(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute the event and return results."""
        ...



# =============================================================================
# Journey Engine
# =============================================================================

class JourneyEngine:
    """Engine for executing journeys and generating timelines.
    
    The journey engine is the orchestrator for temporal event sequences.
    It creates timelines from journey specifications and coordinates
    event execution across products.
    
    Example:
        >>> engine = JourneyEngine(seed=42)
        >>> engine.register_handler("patientsim", "encounter", encounter_handler)
        >>> 
        >>> journey = JourneySpecification(...)
        >>> timeline = engine.create_timeline(patient, journey, start_date)
        >>> 
        >>> # Execute events up to today
        >>> results = engine.execute_timeline(timeline, patient, up_to_date=date.today())
    """
    
    def __init__(self, seed: int | None = None):
        """Initialize the journey engine.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self._rng = random.Random(seed)
        
        # Handlers by product and event type
        self._handlers: dict[str, dict[str, EventHandler]] = {}
        
        # Cross-product trigger handlers
        self._trigger_handlers: dict[str, Callable] = {}
        
        # Active timelines for cross-product coordination
        self._active_timelines: dict[str, Timeline] = {}
    
    def register_handler(
        self,
        product: str,
        event_type: str,
        handler: EventHandler
    ) -> None:
        """Register an event handler for a product/event type combination.
        
        Args:
            product: Product identifier (e.g., "patientsim", "membersim")
            event_type: Event type string
            handler: Callable that handles the event
        """
        if product not in self._handlers:
            self._handlers[product] = {}
        self._handlers[product][event_type] = handler
    
    def register_trigger_handler(
        self,
        target_product: str,
        handler: Callable[[str, TriggerSpec, dict], None]
    ) -> None:
        """Register handler for cross-product triggers.
        
        Args:
            target_product: Product that receives triggers
            handler: Function to handle trigger dispatch
        """
        self._trigger_handlers[target_product] = handler
    
    def create_timeline(
        self,
        entity: Any,
        entity_type: str,
        journey: JourneySpecification,
        start_date: date | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> Timeline:
        """Create a timeline for an entity from a journey specification.
        
        Args:
            entity: The entity (patient, member, etc.)
            entity_type: Type identifier for the entity
            journey: Journey specification to use
            start_date: When to start the timeline
            parameters: Override journey parameters
            
        Returns:
            Timeline with scheduled events
        """
        # Determine entity ID
        entity_id = self._get_entity_id(entity)
        
        # Create timeline
        timeline_start = start_date or date.today()
        timeline = Timeline(
            entity_id=entity_id,
            entity_type=entity_type,
            journey_ids=[journey.journey_id],
            start_date=timeline_start,
        )
        
        # Build context for condition evaluation
        context = self._build_context(entity, entity_type, parameters or {})
        
        # Schedule events
        scheduled_events: dict[str, date] = {}
        current_date = timeline_start
        
        for event_def in journey.events:
            # Check probability
            if event_def.probability < 1.0:
                if self._rng.random() > event_def.probability:
                    continue
            
            # Check conditions
            if not self._evaluate_conditions(event_def.conditions, context):
                continue
            
            # Calculate scheduled date
            if event_def.depends_on and event_def.depends_on in scheduled_events:
                base_date = scheduled_events[event_def.depends_on]
            else:
                base_date = current_date
            
            # Apply delay with seed for reproducibility
            event_seed = self._derive_seed(entity_id, event_def.event_id)
            delay = event_def.delay.to_timedelta(event_seed)
            event_date = base_date + delay
            
            # Create timeline event
            timeline_event_id = self._generate_event_id(entity_id, event_def.event_id)
            timeline_event = TimelineEvent(
                timeline_event_id=timeline_event_id,
                journey_id=journey.journey_id,
                event_definition_id=event_def.event_id,
                scheduled_date=event_date,
                event_type=event_def.event_type,
                event_name=event_def.name,
                product=event_def.product,
            )
            
            timeline.add_event(timeline_event)
            scheduled_events[event_def.event_id] = event_date
            
            # Update current_date for non-dependent events
            if not event_def.depends_on:
                current_date = event_date
        
        # Set end date
        if timeline.events:
            timeline.end_date = max(e.scheduled_date for e in timeline.events)
        
        # Register as active timeline
        self._active_timelines[timeline.entity_id] = timeline
        
        return timeline

    
    def execute_event(
        self,
        timeline: Timeline,
        event: TimelineEvent,
        entity: Any,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute a single event from a timeline.
        
        Args:
            timeline: The entity's timeline
            event: The event to execute
            entity: The entity
            context: Additional context
            
        Returns:
            Execution result dict
        """
        product = event.product
        event_type = event.event_type
        
        # Find handler
        if product not in self._handlers or event_type not in self._handlers[product]:
            return {"status": "skipped", "reason": f"No handler for {product}/{event_type}"}
        
        handler = self._handlers[product][event_type]
        
        try:
            result = handler(entity, event, context or {})
            timeline.mark_executed(event.timeline_event_id, result)
            
            # Process triggers
            self._process_triggers(event, result, context or {})
            
            return {"status": "executed", "outputs": result}
        except Exception as e:
            event.status = "failed"
            return {"status": "failed", "error": str(e)}
    
    def execute_timeline(
        self,
        timeline: Timeline,
        entity: Any,
        up_to_date: date | None = None,
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute all pending events on a timeline up to a date.
        
        Args:
            timeline: Timeline to execute
            entity: The entity
            up_to_date: Execute events up to this date
            context: Additional context
            
        Returns:
            List of execution results
        """
        results = []
        target_date = up_to_date or date.max
        
        for event in timeline.get_events_up_to(target_date):
            result = self.execute_event(timeline, event, entity, context)
            results.append({
                "event_id": event.timeline_event_id,
                "event_type": event.event_type,
                "scheduled_date": event.scheduled_date.isoformat(),
                **result,
            })
        
        return results
    
    def _process_triggers(
        self,
        event: TimelineEvent,
        result: dict[str, Any],
        context: dict[str, Any]
    ) -> None:
        """Process cross-product triggers from an executed event."""
        # This would dispatch to trigger handlers for cross-product coordination
        # Implementation depends on product-specific trigger definitions
        pass
    
    def _build_context(
        self,
        entity: Any,
        entity_type: str,
        parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """Build context dict for condition evaluation."""
        context = {
            "entity_type": entity_type,
            "params": parameters,
        }
        
        # Extract entity attributes if available
        if hasattr(entity, "__dict__"):
            context["entity"] = entity.__dict__
        elif hasattr(entity, "dict"):
            context["entity"] = entity.dict()
        elif isinstance(entity, dict):
            context["entity"] = entity
        
        return context
    
    def _evaluate_conditions(
        self,
        conditions: list[EventCondition],
        context: dict[str, Any]
    ) -> bool:
        """Evaluate all conditions (AND logic)."""
        return all(cond.evaluate(context) for cond in conditions)
    
    def _get_entity_id(self, entity: Any) -> str:
        """Extract entity ID from entity."""
        # Try common ID field names
        for field in ["entity_id", "patient_id", "member_id", "id"]:
            if hasattr(entity, field):
                return str(getattr(entity, field))
            if isinstance(entity, dict) and field in entity:
                return str(entity[field])
        
        # Fallback to hash
        return hashlib.md5(str(entity).encode()).hexdigest()[:12]
    
    def _derive_seed(self, entity_id: str, event_id: str) -> int:
        """Derive a deterministic seed from entity and event IDs."""
        combined = f"{self.seed or 0}:{entity_id}:{event_id}"
        return int(hashlib.md5(combined.encode()).hexdigest()[:8], 16)
    
    def _generate_event_id(self, entity_id: str, event_def_id: str) -> str:
        """Generate unique timeline event ID."""
        return f"{entity_id}_{event_def_id}_{self._derive_seed(entity_id, event_def_id)}"



# =============================================================================
# Convenience Functions
# =============================================================================

def create_journey_engine(seed: int | None = None) -> JourneyEngine:
    """Create a journey engine with default configuration.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        Configured JourneyEngine instance
    """
    return JourneyEngine(seed=seed)


def create_simple_journey(
    journey_id: str,
    name: str,
    events: list[dict[str, Any]],
    products: list[str] | None = None,
) -> JourneySpecification:
    """Create a simple journey from a list of event dicts.
    
    Args:
        journey_id: Unique identifier
        name: Human-readable name
        events: List of event definitions
        products: Target products
        
    Returns:
        JourneySpecification
        
    Example:
        >>> journey = create_simple_journey(
        ...     "diabetic-first-year",
        ...     "First Year of Diabetic Care",
        ...     events=[
        ...         {"event_id": "e1", "name": "Initial Diagnosis", 
        ...          "event_type": "diagnosis", "delay": {"days": 0}},
        ...         {"event_id": "e2", "name": "A1C Test", 
        ...          "event_type": "lab_order", "delay": {"days": 7}, "depends_on": "e1"},
        ...     ]
        ... )
    """
    event_defs = []
    for event_dict in events:
        # Convert delay dict to DelaySpec if needed
        if "delay" in event_dict and isinstance(event_dict["delay"], dict):
            event_dict["delay"] = DelaySpec(**event_dict["delay"])
        
        # Convert conditions
        if "conditions" in event_dict:
            event_dict["conditions"] = [
                EventCondition(**c) if isinstance(c, dict) else c
                for c in event_dict["conditions"]
            ]
        
        event_defs.append(EventDefinition(**event_dict))
    
    return JourneySpecification(
        journey_id=journey_id,
        name=name,
        products=products or ["patientsim"],
        events=event_defs,
    )


# =============================================================================
# Built-in Journey Templates
# =============================================================================

JOURNEY_TEMPLATES = {
    "diabetic-first-year": {
        "journey_id": "diabetic-first-year",
        "name": "First Year of Diabetic Care",
        "description": "Standard care journey for newly diagnosed Type 2 diabetes",
        "products": ["patientsim", "membersim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "initial_dx",
                "name": "Initial Diabetes Diagnosis",
                "event_type": "diagnosis",
                "product": "patientsim",
                "delay": {"days": 0},
                "parameters": {"icd10": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
            },
            {
                "event_id": "initial_a1c",
                "name": "Initial A1C Test",
                "event_type": "lab_order",
                "product": "patientsim",
                "delay": {"days": 0, "days_min": 0, "days_max": 7, "distribution": "uniform"},
                "depends_on": "initial_dx",
                "parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"},
            },
            {
                "event_id": "metformin_start",
                "name": "Start Metformin",
                "event_type": "medication_order",
                "product": "patientsim",
                "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
                "depends_on": "initial_dx",
                "parameters": {"rxnorm": "860975", "drug_name": "Metformin 500 MG"},
            },
            {
                "event_id": "followup_1",
                "name": "3-Month Follow-up",
                "event_type": "encounter",
                "product": "patientsim",
                "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
                "depends_on": "initial_dx",
            },
            {
                "event_id": "followup_a1c",
                "name": "3-Month A1C",
                "event_type": "lab_order",
                "product": "patientsim",
                "delay": {"days": 0},
                "depends_on": "followup_1",
            },
            {
                "event_id": "quality_gap",
                "name": "A1C Gap Identified",
                "event_type": "gap_identified",
                "product": "membersim",
                "delay": {"days": 30},
                "depends_on": "initial_dx",
                "probability": 0.3,
                "parameters": {"measure": "CDC", "description": "A1C not completed within 90 days"},
            },
        ],
    },
    
    "new-member-onboarding": {
        "journey_id": "new-member-onboarding",
        "name": "New Member Onboarding",
        "description": "Standard journey for new health plan enrollment",
        "products": ["membersim"],
        "duration_days": 90,
        "events": [
            {
                "event_id": "enrollment",
                "name": "New Enrollment",
                "event_type": "new_enrollment",
                "product": "membersim",
                "delay": {"days": 0},
            },
            {
                "event_id": "id_card",
                "name": "ID Card Generated",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 3, "days_min": 2, "days_max": 5, "distribution": "uniform"},
                "depends_on": "enrollment",
            },
            {
                "event_id": "welcome_call",
                "name": "Welcome Call",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 14, "days_min": 7, "days_max": 21, "distribution": "uniform"},
                "depends_on": "enrollment",
                "probability": 0.6,
            },
            {
                "event_id": "hra",
                "name": "Health Risk Assessment",
                "event_type": "milestone",
                "product": "membersim",
                "delay": {"days": 30, "days_min": 14, "days_max": 60, "distribution": "uniform"},
                "depends_on": "enrollment",
                "probability": 0.4,
            },
        ],
    },
}


def get_journey_template(template_name: str) -> JourneySpecification:
    """Get a built-in journey template.
    
    Args:
        template_name: Name of the template
        
    Returns:
        JourneySpecification
        
    Raises:
        ValueError: If template not found
    """
    if template_name not in JOURNEY_TEMPLATES:
        available = ", ".join(JOURNEY_TEMPLATES.keys())
        raise ValueError(f"Template '{template_name}' not found. Available: {available}")
    
    template = JOURNEY_TEMPLATES[template_name]
    return create_simple_journey(
        journey_id=template["journey_id"],
        name=template["name"],
        events=template["events"],
        products=template.get("products"),
    )
