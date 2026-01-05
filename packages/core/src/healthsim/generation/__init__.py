"""Data generation framework.

This module provides base classes and utilities for generating
synthetic data with reproducibility support.

The two-phase architecture:
  Phase 1 (Building): Conversational → ProfileSpecification JSON
  Phase 2 (Execution): ProfileSpecification → Generated Data
"""

from healthsim.generation.base import BaseGenerator, PersonGenerator
from healthsim.generation.cohort import (
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
)
from healthsim.generation.distributions import (
    AgeDistribution,
    AgeBandDistribution,
    CategoricalDistribution,
    ConditionalDistribution,
    ExplicitDistribution,
    LogNormalDistribution,
    NormalDistribution,
    UniformDistribution,
    WeightedChoice,
    create_distribution,
)
from healthsim.generation.profile_schema import (
    ClinicalSpec,
    ConditionSpec,
    CoverageSpec,
    DemographicsSpec,
    DistributionSpec,
    DistributionType,
    GenerationSpec,
    GeographyReference,
    OutputSpec,
    ProfileSpecification,
    PROFILE_TEMPLATES,
)
from healthsim.generation.profile_executor import (
    ExecutionResult,
    GeneratedEntity,
    HierarchicalSeedManager,
    ProfileExecutor,
    ValidationMetric,
    ValidationReport,
    execute_profile,
)
from healthsim.generation.reproducibility import SeedManager

__all__ = [
    # Generators
    "BaseGenerator",
    "PersonGenerator",
    "CohortGenerator",
    "CohortConstraints",
    "CohortProgress",
    # Distributions
    "WeightedChoice",
    "NormalDistribution",
    "UniformDistribution",
    "AgeDistribution",
    "LogNormalDistribution",
    "CategoricalDistribution",
    "AgeBandDistribution",
    "ExplicitDistribution",
    "ConditionalDistribution",
    "create_distribution",
    # Profile Schema
    "ProfileSpecification",
    "GenerationSpec",
    "DemographicsSpec",
    "ClinicalSpec",
    "CoverageSpec",
    "ConditionSpec",
    "DistributionSpec",
    "DistributionType",
    "GeographyReference",
    "OutputSpec",
    "PROFILE_TEMPLATES",
    # Profile Executor
    "ProfileExecutor",
    "ExecutionResult",
    "GeneratedEntity",
    "HierarchicalSeedManager",
    "ValidationReport",
    "ValidationMetric",
    "execute_profile",
    # Reproducibility
    "SeedManager",
]
