# NetworkSim

> Generate realistic provider network data including healthcare providers, facilities, pharmacies, and network configurations.

## What NetworkSim Does

NetworkSim is the **provider network** engine of HealthSim. It has two distinct roles:

1. **Reference Knowledge**: Domain expertise about network types (HMO, PPO), plan structures, pharmacy benefits, and utilization management
2. **Synthetic Generation**: Create realistic provider entities with valid NPI formats, taxonomy codes, and network affiliations

When PatientSim needs a cardiologist for a referral or RxMemberSim needs a dispensing pharmacy, NetworkSim provides properly structured entities that make the data realistic.

## Quick Start

**Simple generation:**
```
Generate a cardiologist in Houston
Generate a community hospital with 200 beds
Generate a retail pharmacy chain location
```

**Network structures:**
```
Generate an HMO network with 50 PCPs and specialty referral requirements
Generate a tiered PPO network with in-network and OON providers
```

**Integration:**
```
Generate a provider for this cardiology encounter
```

See [hello-healthsim examples](../../hello-healthsim/examples/networksim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Provider Generation** | Physicians with NPIs, specialties, credentials | [synthetic/synthetic-provider.md](synthetic/synthetic-provider.md) |
| **Facility Generation** | Hospitals, ASCs, imaging centers | [synthetic/synthetic-facility.md](synthetic/synthetic-facility.md) |
| **Pharmacy Generation** | Retail, specialty, mail-order pharmacies | [synthetic/synthetic-pharmacy.md](synthetic/synthetic-pharmacy.md) |
| **Network Configuration** | HMO, PPO, tiered network structures | [synthetic/synthetic-network.md](synthetic/synthetic-network.md) |
| **Plan Structures** | Benefit designs, cost sharing | [reference/plan-structures.md](reference/plan-structures.md) |
| **Pharmacy Benefits** | Formulary tiers, PA requirements | [reference/pharmacy-benefit-concepts.md](reference/pharmacy-benefit-concepts.md) |

## Skill Organization

NetworkSim uses a four-category organization:

### Reference Knowledge (`reference/`)
Domain expertise about healthcare networks:
- [network-types.md](reference/network-types.md) - HMO, PPO, EPO, POS explained
- [plan-structures.md](reference/plan-structures.md) - Benefit design patterns
- [pharmacy-benefit-concepts.md](reference/pharmacy-benefit-concepts.md) - PBM operations
- [network-adequacy.md](reference/network-adequacy.md) - Regulatory requirements

### Synthetic Generation (`synthetic/`)
Create provider entities:
- [synthetic-provider.md](synthetic/synthetic-provider.md) - Physicians, NPIs
- [synthetic-facility.md](synthetic/synthetic-facility.md) - Hospitals, ASCs
- [synthetic-pharmacy.md](synthetic/synthetic-pharmacy.md) - Pharmacy locations
- [synthetic-network.md](synthetic/synthetic-network.md) - Network configurations

### Patterns & Templates (`patterns/`)
Reusable network patterns:
- [hmo-network-pattern.md](patterns/hmo-network-pattern.md) - Closed network with gatekeeping
- [ppo-network-pattern.md](patterns/ppo-network-pattern.md) - Open access with cost differentials
- [tiered-network-pattern.md](patterns/tiered-network-pattern.md) - Multi-tier provider arrangements

### Cross-Product Integration (`integration/`)
Connecting with other products:
- [provider-for-encounter.md](integration/provider-for-encounter.md) - PatientSim integration
- [network-for-member.md](integration/network-for-member.md) - MemberSim integration
- [pharmacy-for-rx.md](integration/pharmacy-for-rx.md) - RxMemberSim integration

## Output Entities

| Entity | Key Fields | Format |
|--------|------------|--------|
| **Provider** | NPI, name, specialty, taxonomy, credentials | JSON |
| **Facility** | NPI, name, type, address, bed count | JSON |
| **Pharmacy** | NCPDP ID, NPI, name, type, address | JSON |
| **Network** | ID, type, providers, facilities | JSON |
| **Plan** | ID, network, benefits, cost sharing | JSON |

## Integration with Other Products

| Product | Integration | Skill |
|---------|-------------|-------|
| **PatientSim** | Provider for encounter | [provider-for-encounter.md](integration/provider-for-encounter.md) |
| **MemberSim** | Network status for adjudication | [network-for-member.md](integration/network-for-member.md) |
| **RxMemberSim** | Pharmacy for prescription | [pharmacy-for-rx.md](integration/pharmacy-for-rx.md) |
| **TrialSim** | Investigator site | [site-for-trial.md](integration/site-for-trial.md) |

## NetworkSim Public vs Private

NetworkSim exists in two versions:

| Aspect | NetworkSim (Public) | NetworkSim-Local (Private) |
|--------|---------------------|----------------------------|
| **Repository** | healthsim-workspace | networksim-local |
| **Purpose** | Synthetic generation | Real data lookup |
| **NPIs** | Valid format, synthetic | Actual registered NPIs |
| **Use Case** | Demos, testing | Research, validation |

See [NetworkSim Dual-Version Guide](../../docs/networksim-dual-version.md) for details.

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim NetworkSim Examples](../../hello-healthsim/examples/networksim-examples.md)
- [NetworkSim Dual-Version Architecture](../../docs/networksim-dual-version.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration)

---

*NetworkSim generates synthetic provider data only. For real NPI data, see NetworkSim-Local.*
