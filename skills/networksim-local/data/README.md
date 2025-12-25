# NetworkSim-Local Data Directory

This directory contains downloaded public healthcare data files. **These files are NOT committed to git.**

---

## Data Sources

### 1. NPPES NPI Registry

**Download URL**: https://download.cms.gov/nppes/NPI_Files.html

**Files**:
- `nppes/npidata_pfile_YYYYMMDD-YYYYMMDD.csv` (~9GB extracted)
- `nppes/othername_pfile_*.csv`
- `nppes/pl_pfile_*.csv` (Practice locations)
- `nppes/endpoint_pfile_*.csv`

**Download Command**:
```bash
curl -o nppes/nppes_full.zip \
  "https://download.cms.gov/nppes/NPPES_Data_Dissemination_November_2025.zip"
unzip nppes/nppes_full.zip -d nppes/
```

---

### 2. NUCC Taxonomy Codes

**Download URL**: https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57

**Files**:
- `taxonomy/nucc_taxonomy.csv`

**Note**: Requires form submission on NUCC website. Download manually.

---

### 3. CMS Provider of Services

**Download URL**: https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities

**Files**:
- `cms-pos/provider_of_services.csv`

---

## Directory Structure

```
data/
├── README.md            # This file (committed)
├── .gitignore           # Excludes data files (committed)
├── nppes/               # NPPES NPI Registry files
│   └── (downloaded CSV files)
├── taxonomy/            # NUCC Taxonomy codes
│   └── (downloaded CSV files)
├── cms-pos/             # CMS Provider of Services
│   └── (downloaded CSV files)
└── networksim-local.duckdb  # Processed database
```

---

## Setup Instructions

### Option A: Automated Download

```bash
cd skills/networksim-local
python setup/download-nppes.py
python setup/download-taxonomy.py
python setup/download-cms-pos.py
python setup/build-local-db.py
```

### Option B: Manual Download

1. Download NPPES from CMS website
2. Download Taxonomy from NUCC website
3. Download POS from data.cms.gov
4. Run `python setup/build-local-db.py`

---

## Estimated Sizes

| File | Raw Size | After Filtering |
|------|----------|-----------------|
| NPPES Full | ~9 GB | ~700 MB (Top 10 states) |
| Taxonomy | ~500 KB | ~500 KB (no filtering) |
| CMS POS | ~50 MB | ~50 MB (no filtering) |
| DuckDB Database | - | ~800 MB |

---

## Update Schedule

| Source | Frequency | Action |
|--------|-----------|--------|
| NPPES | Monthly | Re-download full file |
| Taxonomy | Semi-annual | Check Jan/Jul |
| CMS POS | Quarterly | Check for updates |

---

## Verification

After download, verify with:

```bash
python setup/validate-db.py
```

Expected output:
```
NPPES: 3,000,000+ records
Taxonomy: 900+ codes
Facilities: 50,000+ records
Database: networksim-local.duckdb (valid)
```
