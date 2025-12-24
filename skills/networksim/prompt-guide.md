---
name: networksim-prompt-guide
description: |
  Example prompts for using NetworkSim skills effectively. Templates for
  network reference, provider generation, facility generation, pharmacy
  generation, and cross-product integration scenarios.
---

# NetworkSim Prompt Guide

## Overview

This guide provides example prompts for using NetworkSim skills effectively. Use these templates as starting points for network reference queries and synthetic entity generation.

**Organization**:
1. Reference Knowledge Prompts - Learn concepts
2. Synthetic Generation Prompts - Create entities
3. Cross-Product Integration Prompts - Enhance other products
4. Advanced Prompts - Complex scenarios

---

## Reference Knowledge Prompts

### Network Type Explanations

```
Explain the difference between HMO and PPO networks
```
**Expected**: Comprehensive comparison table with cost/flexibility tradeoffs

```
What are the key characteristics of an EPO plan?
```
**Expected**: EPO definition, how it differs from HMO and PPO, when to use

```
When would a patient choose a POS plan over an HMO?
```
**Expected**: POS advantages, point-of-service decision explanation, cost implications

```
Explain HDHP plans and HSA eligibility requirements
```
**Expected**: HDHP thresholds, HSA rules, triple tax advantage, contribution limits

```
Compare all five major network types in a table
```
**Expected**: HMO, PPO, EPO, POS, HDHP comparison across key dimensions

```
What is a narrow network and why do they exist?
```
**Expected**: Narrow/tiered network concept, cost savings, access tradeoffs

---

### Plan Structure Concepts

```
What components make up a typical health plan benefit structure?
```
**Expected**: Deductibles, copays, coinsurance, OOP max explanation with examples

```
Explain the difference between in-network and out-of-network benefits
```
**Expected**: Cost sharing differences, balance billing, UCR, member responsibility

```
How do tiered networks work?
```
**Expected**: Tier structure, cost incentives, high-performance network concept

```
What's the difference between a copay and coinsurance?
```
**Expected**: Fixed vs percentage cost sharing, when each applies, examples

```
Explain how deductibles and out-of-pocket maximums work together
```
**Expected**: Accumulator relationship, family vs individual, embedded vs aggregate

```
What are the ACA metal tiers (Bronze, Silver, Gold, Platinum)?
```
**Expected**: Actuarial value explanation, cost sharing patterns by tier

---

### Pharmacy Benefit Concepts

```
Explain pharmacy benefit tier structures
```
**Expected**: 4-5 tier explanation, cost sharing by tier, typical drugs in each

```
What's the difference between open and closed formularies?
```
**Expected**: Formulary types, coverage implications, exception processes

```
How do preferred pharmacy networks work?
```
**Expected**: Preferred vs non-preferred, cost incentives, 90-day retail

```
Explain specialty pharmacy vs retail pharmacy
```
**Expected**: Specialty characteristics, limited distribution, hub model, services

```
What is a formulary and how is it developed?
```
**Expected**: P&T committee, clinical criteria, tier placement, rebate considerations

```
Explain pharmacy accumulators vs copay assistance
```
**Expected**: Manufacturer copay cards, accumulator programs, affordability

---

### PBM Operations

```
How does a PBM process pharmacy claims?
```
**Expected**: Claim flow, BIN/PCN routing, real-time adjudication steps

```
What's the relationship between a health plan and PBM?
```
**Expected**: Carve-out vs carve-in, PBM services, contract types

```
Explain the formulary management process
```
**Expected**: P&T committee, clinical review, tier placement, rebate negotiation

```
What is BIN and PCN in pharmacy claims?
```
**Expected**: Bank Identification Number, Processor Control Number, routing

```
How do pharmacy rebates work?
```
**Expected**: Manufacturer rebates, PBM role, pass-through vs spread

```
Explain mail order pharmacy benefits
```
**Expected**: 90-day supply, cost savings, mandatory vs optional mail

---

### Utilization Management

```
What is prior authorization and when is it required?
```
**Expected**: PA process, common PA drugs, approval criteria, turnaround times

```
Explain step therapy requirements
```
**Expected**: Step therapy concept, first-line/second-line, fail-first, exceptions

```
How do quantity limits work?
```
**Expected**: QL types (safety, cost), days supply, dose limits, override process

```
What is a formulary exception and how does it work?
```
**Expected**: Exception types, medical necessity, appeal process

```
Explain prior authorization for specialty drugs
```
**Expected**: Clinical criteria, diagnosis requirements, lab requirements

---

### Specialty Pharmacy Concepts

```
What makes a drug a specialty medication?
```
**Expected**: Cost threshold, complexity, distribution, patient support needs

```
Explain the specialty pharmacy hub model
```
**Expected**: Hub services, patient coordination, benefits investigation

```
What are REMS programs and how do they affect pharmacy?
```
**Expected**: Risk Evaluation and Mitigation Strategies, certification, dispensing

```
How does limited distribution work for specialty drugs?
```
**Expected**: Manufacturer control, exclusive networks, access implications

```
What services do specialty pharmacies provide beyond dispensing?
```
**Expected**: Care coordination, adherence programs, side effect management

---

### Network Adequacy

```
What is network adequacy and why does it matter?
```
**Expected**: Access standards, regulatory requirements, member impact

```
Explain time and distance standards for network adequacy
```
**Expected**: Urban/suburban/rural standards, specialty-specific, state variations

```
What are provider-to-member ratios?
```
**Expected**: PCP ratio, specialist ratio, calculation, adequacy thresholds

```
What are essential community providers?
```
**Expected**: FQHC, safety net, ACA requirements, network inclusion

---

## Synthetic Generation Prompts

### Provider Generation

[To be completed in Phase 5 - 10+ example prompts with variations]

**Basic Generation**:
```
Generate a primary care physician in Chicago
```

**Specialty Specific**:
```
Generate an interventional cardiologist in Houston, Texas
```

**With Credentials**:
```
Generate a board-certified endocrinologist with full credentials
```

**Organization Provider**:
```
Generate a multi-specialty physician group practice in Phoenix
```

[Additional prompts to be added in Phase 5]

---

### Facility Generation

[To be completed in Phase 5 - 10+ example prompts]

**Basic Hospital**:
```
Generate a 200-bed community hospital in suburban Dallas
```

**Specialty Facility**:
```
Generate an ambulatory surgery center specializing in orthopedics
```

**Academic Medical Center**:
```
Generate a Level 1 trauma center affiliated with a medical school
```

[Additional prompts to be added in Phase 5]

---

### Pharmacy Generation

[To be completed in Phase 5 - 10+ example prompts]

**Retail Pharmacy**:
```
Generate a CVS pharmacy in San Diego
```

**Specialty Pharmacy**:
```
Generate a specialty pharmacy for oncology medications
```

**Mail Order**:
```
Generate a mail order pharmacy operation
```

[Additional prompts to be added in Phase 5]

---

### Network Configuration

[To be completed in Phase 5 - 5+ example prompts]

**HMO Network**:
```
Generate an HMO network configuration for a regional health plan
```

**PPO Network**:
```
Generate a broad PPO network covering the Texas Triangle
```

[Additional prompts to be added in Phase 5]

---

## Cross-Product Integration Prompts

### PatientSim Integration

[To be completed in Phase 5]

```
Generate a provider for this heart failure patient's cardiology referral
```

```
Generate an attending physician for this emergency department encounter
```

---

### MemberSim Integration

[To be completed in Phase 5]

```
Generate network context for this member's PPO plan
```

```
Add benefit structure to this member's claim
```

---

### RxMemberSim Integration

[To be completed in Phase 5]

```
Generate a dispensing pharmacy for this specialty prescription
```

```
What pharmacy type should dispense this Humira prescription?
```

---

### TrialSim Integration

[To be completed in Phase 5]

```
Generate a trial site facility for this Phase 3 oncology study
```

```
Generate a principal investigator for this cardiology trial
```

---

### PopulationSim Integration

[To be completed in Phase 5]

```
Generate providers distributed across Harris County proportional to population
```

```
Identify network adequacy gaps in this rural county
```

---

## Advanced Prompts

[To be completed in Phase 5]

### Multi-Entity Generation

```
Generate a complete cardiology practice with 5 physicians and affiliated hospital
```

### Network Adequacy Analysis

```
Analyze this network for adequacy in Maricopa County, Arizona
```

### Complex Scenarios

```
Generate a specialty pharmacy network for a PBM covering all 50 states
```

---

## Tips for Effective Prompts

### Be Specific About Geography

✅ Good:
```
Generate a cardiologist in Harris County, Texas
```

❌ Avoid:
```
Generate a doctor in Texas
```

**Why**: More specific geography produces more realistic addresses and affiliations.

---

### Specify Specialty When Relevant

✅ Good:
```
Generate an interventional cardiologist
```

❌ Avoid:
```
Generate a heart doctor
```

**Why**: Specific specialties map to correct taxonomy codes and realistic credentials.

---

### Include Context for Integration

✅ Good:
```
Generate a provider for this heart failure patient's cardiology referral
[Include patient context]
```

❌ Avoid:
```
Generate a provider
```

**Why**: Context enables matching specialty, geography, and appropriate credentials.

---

### Request Specific Output When Needed

✅ Good:
```
Generate a provider with full taxonomy codes and board certifications
```

❌ Avoid:
```
Generate a provider
```

**Why**: Default output may omit optional fields you need.

---

### Use Multiple Prompts for Complex Needs

✅ Good:
```
1. "Explain specialty pharmacy concepts"
2. "Generate a specialty pharmacy for oncology"
3. "Add this pharmacy to the member's network"
```

❌ Avoid:
```
Do everything related to specialty pharmacy
```

**Why**: Breaking into steps produces more accurate, complete results.

---

## Related Documentation

- [Developer Guide](developer-guide.md) - Technical reference
- [SKILL.md](SKILL.md) - Skill routing
- [Reference Skills](reference/) - Concept explanations
- [Integration Skills](integration/) - Cross-product workflows

---

*Prompt Guide will be expanded in Phase 5 with complete generation and integration examples.*
