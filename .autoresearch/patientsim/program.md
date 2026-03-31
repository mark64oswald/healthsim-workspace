# PatientSim SKILL.md — Autoresearch Program

## Objective
Maximize pass rate on evaluate.py by optimizing skills/patientsim/SKILL.md.

## Target File
`skills/patientsim/SKILL.md`

## Rules
1. One change per experiment.
2. Never modify evaluate.py.
3. Most HealthSim skills are ALREADY over 2000 words — default to tightening
   and refactoring to sub-skill files, not adding content.
4. Preserve frontmatter name and triggers.

## Mutation Strategies
1. Tighten verbose language — say the same thing in fewer words
2. Move detailed tables/examples into sub-skill .md files (no word limit)
3. Add safety guardrails if missing (all data is synthetic, no clinical advice)
4. Add negative examples (what NOT to generate)
5. Strengthen code system references (ICD-10, CPT, LOINC, RxNorm, NDC)
6. Add edge case handling (missing fields, invalid codes, partial data)
