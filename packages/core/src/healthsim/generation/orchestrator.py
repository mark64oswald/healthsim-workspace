"""Profile-to-Journey orchestrator for HealthSim.

This module bridges profile-based entity generation with journey-based
temporal event sequences. It enables:

1. Generate entities from a profile
2. Assign journeys to each entity
3. Create and optionally execute timelines

Example:
    >>> from healthsim.generation import ProfileJourneyOrchestrator
    >>> 
    >>> orchestrator = ProfileJourneyOrchestrator(seed=42)
    >>> result = orchestrator.execute(
    ...     profile="diabetic-senior",
    ...     journey="diabetic-first-year",
    ...     count=100,
    ... )
    >>> print(f"Generated {result.entity_count} entities with {result.event_count} events")
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from healthsim.generation.journey_engine import (
    JourneyEngine,
    JourneySpecification,
    Timeline,
    JOURNEY_TEMPLATES,
    create_simple_journey,
)
from healthsim.generation.profile_executor import (
    ExecutionResult,
    ProfileExecutor,
    GeneratedEntity,
    HierarchicalSeedManager,
)
from healthsim.generation.profile_schema import ProfileSpecification


@dataclass
class EntityWithTimeline:
    """An entity paired with its journey timeline."""
    
    entity: GeneratedEntity
    timeline: Timeline
    journey_ids: list[str] = field(default_factory=list)
    
    @property
    def pending_events(self) -> int:
        """Count of pending events on timeline."""
        return len(self.timeline.get_pending_events())
    
    @property
    def executed_events(self) -> int:
        """Count of executed events."""
        return len([e for e in self.timeline.events if e.status == "executed"])


@dataclass
class OrchestratorResult:
    """Result from orchestrator execution."""
    
    profile_id: str
    journey_ids: list[str]
    seed: int
    
    entities: list[EntityWithTimeline]
    
    duration_seconds: float = 0.0
    
    @property
    def entity_count(self) -> int:
        """Number of entities generated."""
        return len(self.entities)
    
    @property
    def event_count(self) -> int:
        """Total events across all timelines."""
        return sum(len(e.timeline.events) for e in self.entities)
    
    @property
    def pending_events(self) -> int:
        """Total pending events."""
        return sum(e.pending_events for e in self.entities)
    
    def get_events_by_date(self, target_date: date) -> list[tuple[str, Any]]:
        """Get all events scheduled for a specific date.
        
        Returns:
            List of (entity_id, event) tuples
        """
        results = []
        for ent in self.entities:
            for event in ent.timeline.get_events_by_date(target_date):
                results.append((ent.entity.identifiers.get("entity_id", str(ent.entity.index)), event))
        return results


class ProfileJourneyOrchestrator:
    """Orchestrate profile generation with journey assignment.
    
    The orchestrator combines two core capabilities:
    1. Profile execution: Generate entities with demographic/clinical attributes
    2. Journey assignment: Attach temporal event sequences to entities
    
    This enables generating realistic longitudinal healthcare data where
    each entity (patient, member, etc.) has both static attributes and
    a timeline of events.
    
    Example:
        >>> orchestrator = ProfileJourneyOrchestrator(seed=42)
        >>> 
        >>> # Generate with built-in templates
        >>> result = orchestrator.execute(
        ...     profile="diabetic-senior",
        ...     journey="diabetic-first-year",
        ...     count=50,
        ... )
        >>> 
        >>> # Or with custom specs
        >>> result = orchestrator.execute(
        ...     profile=my_profile_spec,
        ...     journey=my_journey_spec,
        ...     count=100,
        ... )
    """
    
    def __init__(
        self,
        seed: int | None = None,
        journey_engine: JourneyEngine | None = None,
    ):
        """Initialize orchestrator.
        
        Args:
            seed: Master seed for reproducibility
            journey_engine: Optional pre-configured journey engine
        """
        self.seed = seed or 42
        self.seed_manager = HierarchicalSeedManager(self.seed)
        self.journey_engine = journey_engine or JourneyEngine(seed=self.seed)
        
        # Registry of profile executors by product
        self._profile_executors: dict[str, type] = {}
    
    def register_executor(self, product: str, executor_class: type) -> None:
        """Register a product-specific profile executor.
        
        Args:
            product: Product identifier (e.g., "patientsim")
            executor_class: Executor class for that product
        """
        self._profile_executors[product] = executor_class
    
    def execute(
        self,
        profile: str | ProfileSpecification | dict,
        journey: str | JourneySpecification | dict | list | None = None,
        count: int | None = None,
        start_date: date | None = None,
        execute_events: bool = False,
        up_to_date: date | None = None,
    ) -> OrchestratorResult:
        """Execute profile generation with journey assignment.
        
        Args:
            profile: Profile template name, spec object, or dict
            journey: Journey template name, spec object, dict, or list of journeys
            count: Override entity count
            start_date: Base date for journey timelines
            execute_events: If True, execute events up to up_to_date
            up_to_date: Date to execute events up to (defaults to start_date)
            
        Returns:
            OrchestratorResult with entities and their timelines
        """
        start_time = time.time()
        
        # Resolve profile
        profile_spec = self._resolve_profile(profile)
        profile_id = profile_spec.id
        
        # Resolve journey(s)
        journeys = self._resolve_journeys(journey) if journey else []
        journey_ids = [j.journey_id for j in journeys]
        
        # Override count if provided
        if count:
            profile_spec.generation.count = count
        
        # Execute profile to generate entities
        executor = ProfileExecutor(profile_spec, seed=self.seed)
        profile_result = executor.execute()
        
        # Assign journeys to entities
        timeline_start = start_date or date.today()
        entities_with_timelines = []
        
        for entity in profile_result.entities:
            # Create entity-specific seed
            entity_seed = self.seed_manager.get_entity_seed(entity.index)
            
            # Build entity context for journey
            entity_context = self._build_entity_context(entity)
            
            # Create combined timeline for all journeys
            combined_timeline = Timeline(
                entity_id=str(entity.index),
                entity_type=self._get_entity_type(profile_spec),
                journey_ids=journey_ids,
                start_date=timeline_start,
            )
            
            # Add events from each journey
            for journey_spec in journeys:
                timeline = self.journey_engine.create_timeline(
                    entity=entity_context,
                    entity_type=self._get_entity_type(profile_spec),
                    journey=journey_spec,
                    start_date=timeline_start,
                )
                # Merge events into combined timeline
                for event in timeline.events:
                    combined_timeline.add_event(event)
            
            # Optionally execute events
            if execute_events and combined_timeline.events:
                exec_date = up_to_date or timeline_start
                self.journey_engine.execute_timeline(
                    combined_timeline,
                    entity_context,
                    up_to_date=exec_date,
                )
            
            entities_with_timelines.append(EntityWithTimeline(
                entity=entity,
                timeline=combined_timeline,
                journey_ids=journey_ids,
            ))
        
        duration = time.time() - start_time
        
        return OrchestratorResult(
            profile_id=profile_id,
            journey_ids=journey_ids,
            seed=self.seed,
            entities=entities_with_timelines,
            duration_seconds=duration,
        )
    
    def _resolve_profile(
        self,
        profile: str | ProfileSpecification | dict,
    ) -> ProfileSpecification:
        """Resolve profile to ProfileSpecification."""
        if isinstance(profile, str):
            # Try to find template - for now create a simple one
            # In real implementation, this would look up registered templates
            return ProfileSpecification(
                id=profile,
                name=profile,
            )
        elif isinstance(profile, dict):
            return ProfileSpecification.model_validate(profile)
        return profile
    
    def _resolve_journeys(
        self,
        journey: str | JourneySpecification | dict | list,
    ) -> list[JourneySpecification]:
        """Resolve journey(s) to list of JourneySpecification."""
        if isinstance(journey, list):
            return [self._resolve_single_journey(j) for j in journey]
        return [self._resolve_single_journey(journey)]
    
    def _resolve_single_journey(
        self,
        journey: str | JourneySpecification | dict,
    ) -> JourneySpecification:
        """Resolve a single journey."""
        if isinstance(journey, str):
            # Look up in templates
            if journey in JOURNEY_TEMPLATES:
                template = JOURNEY_TEMPLATES[journey]
                # Templates are dicts that may have extra fields
                return JourneySpecification.model_validate(template)
            # Create empty journey
            return JourneySpecification(
                journey_id=journey,
                name=journey,
            )
        elif isinstance(journey, dict):
            return JourneySpecification.model_validate(journey)
        return journey
    
    def _build_entity_context(self, entity: GeneratedEntity) -> dict[str, Any]:
        """Build context dict from generated entity."""
        return {
            "entity_id": str(entity.index),
            "age": entity.age,
            "gender": entity.gender,
            "conditions": entity.conditions,
            "coverage_type": entity.coverage_type,
            "attributes": entity.attributes,
            **entity.identifiers,
        }
    
    def _get_entity_type(self, profile: ProfileSpecification) -> str:
        """Determine entity type from profile."""
        products = profile.generation.products
        if "patientsim" in products:
            return "patient"
        elif "membersim" in products:
            return "member"
        elif "rxmembersim" in products:
            return "rx_member"
        elif "trialsim" in products:
            return "subject"
        return "entity"


# =============================================================================
# Convenience Functions
# =============================================================================

def orchestrate(
    profile: str | ProfileSpecification | dict,
    journey: str | JourneySpecification | dict | list | None = None,
    count: int | None = None,
    seed: int | None = None,
    start_date: date | None = None,
) -> OrchestratorResult:
    """Generate entities with journeys in one call.
    
    Args:
        profile: Profile template name or specification
        journey: Journey template name or specification
        count: Number of entities to generate
        seed: Random seed for reproducibility
        start_date: Start date for journey timelines
        
    Returns:
        OrchestratorResult
        
    Example:
        >>> result = orchestrate(
        ...     profile="diabetic-senior",
        ...     journey="diabetic-first-year",
        ...     count=100,
        ...     seed=42,
        ... )
    """
    orchestrator = ProfileJourneyOrchestrator(seed=seed)
    return orchestrator.execute(
        profile=profile,
        journey=journey,
        count=count,
        start_date=start_date,
    )


__all__ = [
    "ProfileJourneyOrchestrator",
    "EntityWithTimeline",
    "OrchestratorResult",
    "orchestrate",
]
