# NetworkSim

> Generate synthetic healthcare provider networks including providers, facilities, pharmacies, and plan configurations with realistic NPI formatting and network structures.

## What NetworkSim Does

NetworkSim is the **provider network** engine of HealthSim. It creates synthetic providers, facilities, and pharmacies with properly formatted NPIs and taxonomy codes. It also provides reference knowledge about network structures (HMO, PPO, tiered networks) and pharmacy benefit designs.

When other HealthSim products need a provider for an encounter, a pharmacy for a prescription, or a facility for a claim, NetworkSim generates the appropriate entity with realistic characteristics.

## Quick Start

**Generate providers:**
```
Generate a cardiologist in Houston, TX
Generate 10 primary care physicians for San Diego County
```

**Generate facilities:**
```
Generate a 200-bed acute care hospital in Phoenix
Generate an ambulatory surgery center
```

**Generate networks:**
```
Generate a PPO network with 500 providers across 3 counties
Generate a tiered pharmacy network
```

See [hello-healthsim examples](../../hello-healthsim/examples/networksim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Reference Knowledge** | Network types, plan structures, pharmacy benefits | [reference/](reference/) |
| **Synthetic Providers** | Physicians, NPs, PAs with NPIs | [synthetic/synthetic-provider.md](synthetic/synthetic-provider.md) |
| **Synthetic Facilities** | Hospitals, ASCs, clinics | [synthetic/synthetic-facility.md](synthetic/synthetic-facility.md) |
| **Synthetic Pharmacies** | Retail, mail-order, specialty | [synthetic/synthetic-pharmacy.md](synthetic/synthetic-pharmacy.md) |
| **Network Patterns** | HMO, PPO, tiered structures | [patterns/](patterns/) |
| **Cross-Product Integration** | Provider entities for other products | [integration/](integration/) |

## Skill Categories

### Reference Knowledge
Domain knowledge about how real networks work:

| Skill | Purpose |
|-------|---------|
| [network-types.md](reference/network-types.md) | HMO, PPO, EPO, POS structures |
| [plan-structures.md](reference/plan-structures.md) | Cost sharing, benefit design |
| [pharmacy-benefit-concepts.md](reference/pharmacy-benefit-concepts.md) | PBM, formulary, tiers |
| [network-adequacy.md](reference/network-adequacy.md) | Access standards, ratios |

### Synthetic Generation
Create realistic healthcare entities:

| Skill | Output |
|-------|--------|
| [synthetic-provider.md](synthetic/synthetic-provider.md) | Provider with NPI, taxonomy, credentials |
| [synthetic-facility.md](synthetic/synthetic-facility.md) | Facility with beds, services, addresses |
| [synthetic-pharmacy.md](synthetic/synthetic-pharmacy.md) | Pharmacy with NCPDP ID, hours, services |
| [synthetic-network.md](synthetic/synthetic-network.md) | Complete network configuration |

### Integration Skills
Provide entities to other HealthSim products:

| Skill | Use Case |
|-------|----------|
| [provider-for-encounter.md](integration/provider-for-encounter.md) | Attending/referring for PatientSim |
| [network-for-member.md](integration/network-for-member.md) | Network status for MemberSim claims |
| [pharmacy-for-rx.md](integration/pharmacy-for-rx.md) | Dispensing pharmacy for RxMemberSim |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | (default) | API testing, integration |
| CSV | "as CSV" | Analytics, spreadsheets |

## Integration with Other Products

| Product | NetworkSim Provides | Example |
|---------|---------------------|---------|
| **PatientSim** | Attending, referring, PCP | Cardiologist for heart failure encounter |
| **MemberSim** | Billing provider, network status | In-network vs OON for adjudication |
| **RxMemberSim** | Dispensing pharmacy | CVS with NCPDP ID for Rx claim |
| **TrialSim** | Site, investigator | PI credentials for trial site |

## Data Architecture

NetworkSim supports two data modes:

| Mode | Skill Prefix | Data Source | Use Case |
|------|--------------|-------------|----------|
| **NetworkSim-Gen** (Default) | Synthetic generation | On-demand by Claude | Demos, tutorials, testing |
| **NetworkSim-DB** (Optional) | DuckDB queries | Real NPPES registry | Research, validation, analytics |

**NetworkSim-Gen** is the default mode, requiring no additional setup. Claude generates synthetic providers with valid NPI format during conversation.

**NetworkSim-DB** is an optional mode for users who need real provider data. It requires downloading the NPPES database (~1.7GB). When available, Claude can query actual registered providers.

See [Data Architecture](../../docs/networksim-dual-version.md) for full details on the dual-mode approach.

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim NetworkSim Examples](../../hello-healthsim/examples/networksim-examples.md)
- [NetworkSim Dual-Version Architecture](../../docs/networksim-dual-version.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration)
- [Code Systems Reference](../../references/code-systems.md)

---

*NetworkSim-Gen generates synthetic provider data. For real NPPES data, enable NetworkSim-DB mode.*
