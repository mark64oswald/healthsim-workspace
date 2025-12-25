# NetworkSim-Local Session 1: Data Research

**Date**: December 25, 2024  
**Status**: Complete  
**Objective**: Analyze available public data sources, define filtering strategy, estimate sizes

---

## Executive Summary

NetworkSim-Local will leverage **real NPPES NPI Registry data** as its primary source, supplemented by **CMS Provider of Services** for facility characteristics and **NUCC Taxonomy codes** for specialty mapping. Unlike NetworkSim (which synthesizes data), NetworkSim-Local provides actual provider information with provenance tracking.

### Key Findings

| Data Source | Availability | Size | Update Frequency |
|-------------|--------------|------|------------------|
| NPPES NPI Registry | ✅ Free/Public | ~1GB ZIP → 9GB CSV | Monthly (full) + Weekly (incremental) |
| CMS Provider of Services | ✅ Free/Public | ~50MB | Quarterly |
| NUCC Taxonomy Codes | ✅ Free/Public | ~500KB CSV | Semi-annual (Jan/Jul) |
| NCPDP Pharmacy Database | ❌ Proprietary | N/A | N/A (commercial license required) |

**Decision**: Use NPPES as unified source for providers, facilities, AND pharmacies (via taxonomy filtering).

---

## Data Source Analysis

### 1. NPPES NPI Registry (Primary Source)

**URL**: https://download.cms.gov/nppes/NPI_Files.html

**What it contains**:
- 8.6+ million provider records (individuals and organizations)
- NPI (10-digit identifier)
- Entity type (1=Individual, 2=Organization)
- Provider name (legal business name or individual name)
- Practice location addresses
- Mailing addresses
- Taxonomy codes (up to 15 per provider)
- Other identifiers (Medicare, Medicaid, etc.)
- Enumeration date
- Deactivation date (if applicable)

**File Structure** (from CMS documentation):
```
Main Data File:
├── npidata_pfile_YYYYMMDD-YYYYMMDD.csv (~9GB)
├── Header file
├── Code Values document (PDF)
└── Readme file (PDF)

Reference Files (since June 2018):
├── othername_pfile_*.csv (Other Names for Type 2 NPIs)
├── pl_pfile_*.csv (Practice Locations - non-primary)
└── endpoint_pfile_*.csv (Electronic endpoints)
```

**Key Fields for NetworkSim-Local**:

| Field | Description | Use Case |
|-------|-------------|----------|
| NPI | 10-digit identifier | Primary key |
| Entity Type Code | 1=Individual, 2=Organization | Filter/categorize |
| Provider Organization Name | Legal business name | Display |
| Provider Last Name | Individual provider | Display |
| Provider First Name | Individual provider | Display |
| Provider Credential Text | MD, DO, NP, etc. | Display/filter |
| Provider Business Practice Location Address | Street, City, State, ZIP | Geographic queries |
| Healthcare Provider Taxonomy Code_1-15 | Specialty codes | Specialty filtering |
| Healthcare Provider Primary Taxonomy Switch_1-15 | Y/N/X | Identify primary specialty |
| Provider Enumeration Date | When NPI assigned | Recency filtering |
| NPI Deactivation Date | If deactivated | Exclude inactive |

**Version Note**: As of December 2024, CMS offers two versions:
- **Version 1**: Original field lengths
- **Version 2 (V.2)**: Extended field lengths for First Name and Legal Business Name

**Recommendation**: Use Version 1 for compatibility; field length rarely an issue.

---

### 2. CMS Provider of Services (Facility Enrichment)

**URL**: https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities

**What it contains**:
- Medicare-certified facilities
- CMS Certification Number (CCN)
- Facility type and subtype
- Bed counts
- Ownership type
- Accreditation status
- Geographic location

**Key Fields**:
- CCN (links to Medicare claims)
- Facility Name
- Address
- Bed Count
- Facility Type (Hospital, SNF, HHA, etc.)
- Ownership Type (For-profit, Non-profit, Government)
- Provider Subtype

**Use Case**: Enrich organization NPIs with facility characteristics (bed count, ownership, accreditation).

---

### 3. NUCC Health Care Provider Taxonomy Codes

**URL**: https://taxonomy.nucc.org/ and https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57

**What it contains**:
- Complete taxonomy code hierarchy
- Provider Grouping → Classification → Specialization
- ~900 unique codes
- Definitions and effective dates

**Structure**:
```
Level 1: Provider Grouping (e.g., "Allopathic & Osteopathic Physicians")
  Level 2: Classification (e.g., "Internal Medicine")
    Level 3: Specialization (e.g., "Cardiovascular Disease")
```

**Key Taxonomy Groups for NetworkSim-Local**:

| Grouping Code Prefix | Description |
|---------------------|-------------|
| 101Y-104* | Behavioral Health |
| 111N-1164 | Chiropractic |
| 122300000X-1223X* | Dentistry |
| 152W-156F* | Eye and Vision |
| 163W-167G* | Nursing |
| 207-208* | Allopathic Physicians (MD) |
| 261Q* | Ambulatory Care Facilities |
| 275N-276* | Hospitals |
| 281P-283* | Residential Treatment/SNF |
| 291U-293* | Labs |
| 302F-305* | Eye/Dental/Prosthetic Suppliers |
| 311Z-315* | Nursing/Custodial Care |
| 320-322* | Residential Treatment |
| 331-335* | Suppliers |
| 3336* | Pharmacy |

---

### 4. NCPDP Pharmacy Database (NOT Available)

**Status**: ❌ **Proprietary - Commercial License Required**

The NCPDP dataQ database is the authoritative source for pharmacy identifiers but requires paid subscription. 

**Alternative Strategy**: Filter NPPES for pharmacy-related taxonomy codes:
- `3336C0002X` - Clinic Pharmacy
- `3336C0003X` - Community/Retail Pharmacy
- `3336C0004X` - Compounding Pharmacy
- `3336H0001X` - Home Infusion Therapy Pharmacy
- `3336I0012X` - Institutional Pharmacy
- `3336L0003X` - Long Term Care Pharmacy
- `3336M0002X` - Mail Order Pharmacy
- `3336N0007X` - Nuclear Pharmacy
- `3336S0011X` - Specialty Pharmacy

This gives us real pharmacy NPIs with addresses, which is sufficient for NetworkSim-Local.

---

## Filtering Strategy

### The Challenge

Full NPPES file is **9+ GB** with 8.6+ million records. This is too large to:
1. Store in GitHub repository
2. Load efficiently into DuckDB for real-time queries
3. Keep updated practically

### Proposed Filtering Approach

**Option A: Geographic Subset** (Recommended for MVP)
- Filter to specific states (e.g., California, Texas, New York)
- Provides diverse provider mix
- Reduces size by ~90%

**Option B: Active Providers Only**
- Exclude deactivated NPIs
- Reduces by ~10-15%

**Option C: Primary Care + Common Specialties**
- Filter to specific taxonomy codes
- Risk: May miss needed specialties

**Option D: Combined Strategy** (Recommended)
```sql
-- Active providers only (no deactivation date)
WHERE NPI_Deactivation_Date IS NULL
-- OR specific high-value states
AND Provider_Business_Practice_Location_Address_State_Name IN 
    ('CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI')
```

### Estimated Sizes After Filtering

| Filter Strategy | Est. Records | Est. Size (Parquet) |
|----------------|--------------|---------------------|
| Full file | 8.6M | ~2GB |
| Active only | 7.5M | ~1.8GB |
| Top 10 states, active | 3.0M | ~700MB |
| Top 5 states, active | 1.8M | ~400MB |
| Single state (CA) | 900K | ~200MB |

**Recommendation**: Start with **Top 10 states, active providers** (~700MB Parquet).

---

## Proposed DuckDB Schema

### Core Tables

```sql
-- Main provider table (from NPPES)
CREATE TABLE providers (
    npi VARCHAR(10) PRIMARY KEY,
    entity_type_code TINYINT,  -- 1=Individual, 2=Organization
    
    -- Organization fields (Type 2)
    organization_name VARCHAR(200),
    organization_other_name VARCHAR(200),
    organization_other_name_type VARCHAR(50),
    
    -- Individual fields (Type 1)
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    name_prefix VARCHAR(10),
    name_suffix VARCHAR(10),
    credential VARCHAR(50),
    
    -- Practice location
    practice_address_1 VARCHAR(100),
    practice_address_2 VARCHAR(100),
    practice_city VARCHAR(50),
    practice_state VARCHAR(2),
    practice_zip VARCHAR(15),
    practice_country VARCHAR(2),
    practice_phone VARCHAR(20),
    practice_fax VARCHAR(20),
    
    -- Mailing address
    mailing_address_1 VARCHAR(100),
    mailing_address_2 VARCHAR(100),
    mailing_city VARCHAR(50),
    mailing_state VARCHAR(2),
    mailing_zip VARCHAR(15),
    mailing_country VARCHAR(2),
    mailing_phone VARCHAR(20),
    mailing_fax VARCHAR(20),
    
    -- Metadata
    enumeration_date DATE,
    last_update_date DATE,
    deactivation_date DATE,
    reactivation_date DATE,
    gender VARCHAR(1),
    is_sole_proprietor BOOLEAN,
    is_organization_subpart BOOLEAN,
    parent_organization_lbn VARCHAR(200),
    parent_organization_tin VARCHAR(9),
    
    -- Computed for filtering
    is_active BOOLEAN GENERATED ALWAYS AS (deactivation_date IS NULL)
);

-- Provider taxonomies (normalized from repeating groups)
CREATE TABLE provider_taxonomies (
    npi VARCHAR(10),
    taxonomy_code VARCHAR(10),
    license_number VARCHAR(20),
    license_state VARCHAR(2),
    is_primary BOOLEAN,
    taxonomy_group VARCHAR(100),  -- Joined from taxonomy_codes
    FOREIGN KEY (npi) REFERENCES providers(npi)
);

-- Taxonomy code reference
CREATE TABLE taxonomy_codes (
    code VARCHAR(10) PRIMARY KEY,
    grouping VARCHAR(100),
    classification VARCHAR(100),
    specialization VARCHAR(100),
    definition TEXT,
    effective_date DATE,
    deactivation_date DATE
);

-- Facility enrichment (from CMS POS)
CREATE TABLE facilities (
    ccn VARCHAR(10) PRIMARY KEY,
    npi VARCHAR(10),  -- Link to providers
    facility_name VARCHAR(200),
    facility_type VARCHAR(50),
    facility_subtype VARCHAR(50),
    bed_count INTEGER,
    ownership_type VARCHAR(50),
    address_1 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),
    county_code VARCHAR(5),
    accreditation_status VARCHAR(50),
    certification_date DATE,
    FOREIGN KEY (npi) REFERENCES providers(npi)
);

-- Geographic lookup (for PopulationSim integration)
CREATE TABLE provider_geography (
    npi VARCHAR(10) PRIMARY KEY,
    state_fips VARCHAR(2),
    county_fips VARCHAR(5),
    tract_fips VARCHAR(11),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    FOREIGN KEY (npi) REFERENCES providers(npi)
);
```

### Indexes for Common Queries

```sql
-- Fast lookups
CREATE INDEX idx_providers_state ON providers(practice_state);
CREATE INDEX idx_providers_zip ON providers(practice_zip);
CREATE INDEX idx_providers_city_state ON providers(practice_city, practice_state);
CREATE INDEX idx_providers_org_name ON providers(organization_name);
CREATE INDEX idx_providers_last_name ON providers(last_name);

-- Taxonomy lookups
CREATE INDEX idx_taxonomies_npi ON provider_taxonomies(npi);
CREATE INDEX idx_taxonomies_code ON provider_taxonomies(taxonomy_code);
CREATE INDEX idx_taxonomies_primary ON provider_taxonomies(is_primary);
```

---

## Data Acquisition Steps

### Step 1: Download NPPES Data

```bash
# Create data directory
mkdir -p data/nppes

# Download latest monthly file (~1GB)
curl -o data/nppes/nppes_full.zip \
  "https://download.cms.gov/nppes/NPPES_Data_Dissemination_November_2025.zip"

# Extract
unzip data/nppes/nppes_full.zip -d data/nppes/
```

### Step 2: Download Taxonomy Codes

```bash
mkdir -p data/taxonomy

# Download from NUCC (requires form submission for CSV)
# Manual download from: https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57
```

### Step 3: Download CMS Provider of Services

```bash
mkdir -p data/cms-pos

# Download from data.cms.gov API or manual download
# https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities
```

### Step 4: Filter and Transform

```python
# filter_nppes.py
import duckdb
import pandas as pd

# Connect to DuckDB
con = duckdb.connect('data/networksim-local.duckdb')

# Load NPPES with filtering
con.execute("""
    CREATE TABLE providers AS
    SELECT *
    FROM read_csv_auto('data/nppes/npidata_pfile_*.csv')
    WHERE "NPI Deactivation Date" IS NULL
    AND "Provider Business Practice Location Address State Name" IN 
        ('CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI')
""")

print(f"Loaded {con.execute('SELECT COUNT(*) FROM providers').fetchone()[0]} providers")
```

---

## Cross-Product Integration

### PopulationSim Integration

NetworkSim-Local can leverage PopulationSim's geographic data:

```sql
-- Join provider location to PopulationSim tract data
SELECT 
    p.npi,
    p.practice_city,
    p.practice_state,
    ps.population,
    ps.median_income,
    ps.pct_uninsured
FROM providers p
JOIN populationsim.tract_demographics ps 
    ON p.practice_zip = ps.zip_code  -- Approximate join
WHERE p.practice_state = 'CA'
```

### Entity Correlation

| NetworkSim-Local Entity | Cross-Product Mapping |
|------------------------|----------------------|
| Provider (NPI) | PatientSim: Attending/Referring Physician |
| Facility (CCN) | PatientSim: Service Location |
| Pharmacy (NPI) | RxMemberSim: Dispensing Pharmacy |
| Organization (NPI) | MemberSim: Provider Network |

---

## File Organization

```
skills/networksim-local/
├── SKILL.md                    # Master skill file
├── README.md                   # Product overview
├── developer-guide.md          # Setup and usage
├── SESSION-1-DATA-RESEARCH.md  # This document
│
├── data/                       # .gitignore'd - local only
│   ├── README.md               # Documents download process (committed)
│   ├── .gitignore              # Excludes *.csv, *.parquet, *.duckdb
│   ├── nppes/                  # Raw NPPES files
│   ├── cms-pos/                # CMS Provider of Services
│   ├── taxonomy/               # NUCC taxonomy codes
│   └── networksim-local.duckdb # Processed database
│
├── setup/                      # Download/transform scripts (committed)
│   ├── download-nppes.py
│   ├── download-taxonomy.py
│   ├── download-cms-pos.py
│   ├── filter-providers.py
│   ├── build-local-db.py
│   └── requirements.txt
│
├── skills/                     # Lookup skills
│   ├── provider-lookup.md
│   ├── facility-lookup.md
│   ├── pharmacy-lookup.md
│   ├── specialty-search.md
│   └── geographic-search.md
│
└── queries/                    # SQL queries for DuckDB
    ├── provider-by-npi.sql
    ├── providers-by-geography.sql
    ├── providers-by-specialty.sql
    ├── facilities-by-type.sql
    └── pharmacies-by-location.sql
```

---

## Next Steps (Session 2)

1. **Create Setup Scripts**
   - `download-nppes.py` - Automated NPPES download
   - `download-taxonomy.py` - NUCC taxonomy download
   - `filter-providers.py` - Apply filtering strategy
   - `build-local-db.py` - Create DuckDB database

2. **Create Data Directory Structure**
   - README.md documenting download process
   - .gitignore for data files
   - requirements.txt for Python dependencies

3. **Initial Data Load**
   - Download sample state (California)
   - Validate schema
   - Test basic queries

---

## Success Criteria for Session 1 ✅

- [x] Identified primary data source (NPPES)
- [x] Documented file structure and key fields
- [x] Defined filtering strategy (Top 10 states, active only)
- [x] Estimated filtered data sizes (~700MB)
- [x] Designed DuckDB schema
- [x] Documented data acquisition steps
- [x] Identified cross-product integration points
- [x] Created file organization plan
