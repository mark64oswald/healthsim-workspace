"""Tests for NetworkSim reference data resolver."""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from healthsim.generation.networksim_reference import (
    EntityType,
    FacilityType,
    Provider,
    Facility,
    ProviderSearchCriteria,
    FacilitySearchCriteria,
    NetworkSimResolver,
    TAXONOMY_MAP,
    get_networksim_db_path,
    get_providers_by_geography,
    get_facilities_by_geography,
    assign_provider_to_patient,
    assign_facility_to_patient,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_conn():
    """Create a mock DuckDB connection."""
    conn = MagicMock()
    return conn


@pytest.fixture
def sample_provider_row():
    """Sample provider row from database."""
    return (
        "1234567890",  # npi
        "1",           # entity_type_code (individual)
        "SMITH",       # last_name
        "JOHN",        # first_name
        "A",           # middle_name
        "MD",          # credential
        "M",           # gender
        None,          # organization_name
        "HOUSTON",     # practice_city
        "TX",          # practice_state
        "77001",       # practice_zip
        "123 Main St", # practice_address_1
        "Suite 100",   # practice_address_2
        "713-555-1234", # phone
        "207R00000X",  # taxonomy_1 (internal medicine)
        None,          # taxonomy_2
        None,          # taxonomy_3
    )


@pytest.fixture
def sample_org_provider_row():
    """Sample organization provider row."""
    return (
        "9876543210",
        "2",  # organization
        None, None, None, None, None,
        "HOUSTON MEDICAL CENTER",
        "HOUSTON", "TX", "77002",
        "456 Hospital Way", None,
        "713-555-5678",
        "282N00000X",  # hospital taxonomy
        None, None,
    )


@pytest.fixture
def sample_facility_row():
    """Sample facility row from database."""
    return (
        "450001",           # ccn
        "MEMORIAL HERMANN", # name
        "hospital",         # type
        "HOUSTON",          # city
        "TX",               # state
        "77030",            # zip
        "713-555-0000",     # phone
        500,                # beds
        "acute",            # subtype
    )


# =============================================================================
# Entity Type Tests
# =============================================================================

class TestEntityType:
    """Tests for EntityType enum."""
    
    def test_individual_value(self):
        """Individual entity type has correct value."""
        assert EntityType.INDIVIDUAL.value == "1"
    
    def test_organization_value(self):
        """Organization entity type has correct value."""
        assert EntityType.ORGANIZATION.value == "2"
    
    def test_from_string(self):
        """Can create from string value."""
        assert EntityType("1") == EntityType.INDIVIDUAL
        assert EntityType("2") == EntityType.ORGANIZATION


# =============================================================================
# Provider Data Class Tests
# =============================================================================

class TestProvider:
    """Tests for Provider data class."""
    
    def test_individual_provider(self):
        """Test individual provider creation."""
        provider = Provider(
            npi="1234567890",
            entity_type=EntityType.INDIVIDUAL,
            last_name="SMITH",
            first_name="JOHN",
            credential="MD",
        )
        
        assert provider.npi == "1234567890"
        assert provider.entity_type == EntityType.INDIVIDUAL
        assert provider.display_name == "JOHN SMITH , MD"
    
    def test_organization_provider(self):
        """Test organization provider creation."""
        provider = Provider(
            npi="9876543210",
            entity_type=EntityType.ORGANIZATION,
            organization_name="HOUSTON MEDICAL CENTER",
        )
        
        assert provider.entity_type == EntityType.ORGANIZATION
        assert provider.display_name == "HOUSTON MEDICAL CENTER"
    
    def test_primary_taxonomy(self):
        """Test primary taxonomy property."""
        provider = Provider(
            npi="1234567890",
            entity_type=EntityType.INDIVIDUAL,
            taxonomy_1="207R00000X",
            taxonomy_2="207RC0000X",
        )
        
        assert provider.primary_taxonomy == "207R00000X"
    
    def test_display_name_missing_fields(self):
        """Test display name with missing fields."""
        provider = Provider(
            npi="1234567890",
            entity_type=EntityType.INDIVIDUAL,
        )
        
        assert provider.display_name == "Unknown Provider"
        
        org = Provider(
            npi="9876543210",
            entity_type=EntityType.ORGANIZATION,
        )
        
        assert org.display_name == "Unknown Organization"


# =============================================================================
# Facility Data Class Tests
# =============================================================================

class TestFacility:
    """Tests for Facility data class."""
    
    def test_facility_creation(self):
        """Test facility creation."""
        facility = Facility(
            ccn="450001",
            name="MEMORIAL HERMANN",
            facility_type="hospital",
            city="HOUSTON",
            state="TX",
            beds=500,
        )
        
        assert facility.ccn == "450001"
        assert facility.name == "MEMORIAL HERMANN"
        assert facility.beds == 500
    
    def test_facility_optional_fields(self):
        """Test facility with minimal fields."""
        facility = Facility(
            ccn="123456",
            name="Test Facility",
            facility_type="snf",
        )
        
        assert facility.city is None
        assert facility.beds is None


# =============================================================================
# Taxonomy Map Tests
# =============================================================================

class TestTaxonomyMap:
    """Tests for taxonomy code mapping."""
    
    def test_internal_medicine(self):
        """Internal medicine taxonomy is correct."""
        assert TAXONOMY_MAP["internal_medicine"] == "207R00000X"
    
    def test_cardiology(self):
        """Cardiology taxonomy is correct."""
        assert TAXONOMY_MAP["cardiology"] == "207RC0000X"
    
    def test_nurse_practitioner(self):
        """Nurse practitioner taxonomy is correct."""
        assert TAXONOMY_MAP["nurse_practitioner"] == "363L00000X"
    
    def test_all_keys_lowercase_underscore(self):
        """All keys follow naming convention."""
        for key in TAXONOMY_MAP:
            assert key == key.lower()
            assert " " not in key


# =============================================================================
# NetworkSim Resolver Tests
# =============================================================================

class TestNetworkSimResolver:
    """Tests for NetworkSimResolver."""
    
    def test_find_providers_by_state(self, mock_conn, sample_provider_row):
        """Test finding providers by state."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(state="TX")
        
        assert len(providers) == 1
        assert providers[0].practice_state == "TX"
        
        # Verify query contains state filter
        call_args = mock_conn.execute.call_args
        assert "practice_state = ?" in call_args[0][0]
        assert "TX" in call_args[0][1]
    
    def test_find_providers_by_city(self, mock_conn, sample_provider_row):
        """Test finding providers by city."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(city="Houston")
        
        # Verify case-insensitive city search
        call_args = mock_conn.execute.call_args
        assert "UPPER(practice_city) = UPPER(?)" in call_args[0][0]
    
    def test_find_providers_by_taxonomy(self, mock_conn, sample_provider_row):
        """Test finding providers by taxonomy code."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(taxonomy="207R00000X")
        
        # Verify taxonomy search across all taxonomy fields
        call_args = mock_conn.execute.call_args
        assert "taxonomy_1 = ?" in call_args[0][0]
        assert "taxonomy_2 = ?" in call_args[0][0]
    
    def test_find_providers_entity_type(self, mock_conn, sample_provider_row):
        """Test filtering by entity type."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(entity_type=EntityType.INDIVIDUAL)
        
        call_args = mock_conn.execute.call_args
        assert "entity_type_code = ?" in call_args[0][0]
    
    def test_find_providers_random_sample(self, mock_conn, sample_provider_row):
        """Test random sampling."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        resolver.find_providers(random_sample=True)
        
        call_args = mock_conn.execute.call_args
        assert "ORDER BY RANDOM()" in call_args[0][0]
    
    def test_find_facilities_by_state(self, mock_conn, sample_facility_row):
        """Test finding facilities by state."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        resolver = NetworkSimResolver(mock_conn)
        facilities = resolver.find_facilities(state="TX")
        
        assert len(facilities) == 1
        assert facilities[0].state == "TX"
    
    def test_find_facilities_by_beds(self, mock_conn, sample_facility_row):
        """Test filtering facilities by bed count."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        resolver = NetworkSimResolver(mock_conn)
        facilities = resolver.find_facilities(min_beds=100, max_beds=600)
        
        call_args = mock_conn.execute.call_args
        assert "beds >= ?" in call_args[0][0]
        assert "beds <= ?" in call_args[0][0]
    
    def test_get_provider_by_npi(self, mock_conn, sample_provider_row):
        """Test getting provider by NPI."""
        mock_conn.execute.return_value.fetchone.return_value = sample_provider_row
        
        resolver = NetworkSimResolver(mock_conn)
        provider = resolver.get_provider_by_npi("1234567890")
        
        assert provider is not None
        assert provider.npi == "1234567890"
    
    def test_get_provider_by_npi_not_found(self, mock_conn):
        """Test getting non-existent provider."""
        mock_conn.execute.return_value.fetchone.return_value = None
        
        resolver = NetworkSimResolver(mock_conn)
        provider = resolver.get_provider_by_npi("0000000000")
        
        assert provider is None
    
    def test_get_facility_by_ccn(self, mock_conn, sample_facility_row):
        """Test getting facility by CCN."""
        mock_conn.execute.return_value.fetchone.return_value = sample_facility_row
        
        resolver = NetworkSimResolver(mock_conn)
        facility = resolver.get_facility_by_ccn("450001")
        
        assert facility is not None
        assert facility.ccn == "450001"
    
    def test_count_providers(self, mock_conn):
        """Test counting providers."""
        mock_conn.execute.return_value.fetchone.return_value = (1000,)
        
        resolver = NetworkSimResolver(mock_conn)
        count = resolver.count_providers(state="TX")
        
        assert count == 1000
    
    def test_count_facilities(self, mock_conn):
        """Test counting facilities."""
        mock_conn.execute.return_value.fetchone.return_value = (500,)
        
        resolver = NetworkSimResolver(mock_conn)
        count = resolver.count_facilities(state="TX", facility_type="hospital")
        
        assert count == 500
    
    def test_list_states_with_providers(self, mock_conn):
        """Test listing states."""
        mock_conn.execute.return_value.fetchall.return_value = [
            ("TX", 100000),
            ("CA", 150000),
        ]
        
        resolver = NetworkSimResolver(mock_conn)
        states = resolver.list_states_with_providers()
        
        assert len(states) == 2
        assert states[0]["state"] == "TX"
        assert states[0]["count"] == 100000


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_get_providers_by_geography(self, mock_conn, sample_provider_row):
        """Test get_providers_by_geography function."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        providers = get_providers_by_geography(
            mock_conn,
            state="TX",
            city="Houston",
            specialty="internal_medicine",
        )
        
        assert len(providers) == 1
    
    def test_get_providers_with_taxonomy_code(self, mock_conn, sample_provider_row):
        """Test passing taxonomy code directly."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        providers = get_providers_by_geography(
            mock_conn,
            state="TX",
            specialty="207R00000X",  # Direct code
        )
        
        assert len(providers) == 1
    
    def test_get_facilities_by_geography(self, mock_conn, sample_facility_row):
        """Test get_facilities_by_geography function."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        facilities = get_facilities_by_geography(
            mock_conn,
            state="TX",
            facility_type="hospital",
        )
        
        assert len(facilities) == 1
    
    def test_assign_provider_to_patient(self, mock_conn, sample_provider_row):
        """Test provider assignment."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        provider = assign_provider_to_patient(
            mock_conn,
            patient_state="TX",
            patient_city="Houston",
            seed=42,
        )
        
        assert provider is not None
        assert provider.practice_state == "TX"
    
    def test_assign_provider_fallback_to_state(self, mock_conn, sample_provider_row):
        """Test provider assignment falls back to state level."""
        # First call (city search) returns empty, second (state) returns result
        mock_conn.execute.return_value.fetchall.side_effect = [
            [],  # No results for city
            [sample_provider_row],  # Results for state
        ]
        
        provider = assign_provider_to_patient(
            mock_conn,
            patient_state="TX",
            patient_city="SmallTown",
            seed=42,
        )
        
        assert provider is not None
    
    def test_assign_provider_no_match(self, mock_conn):
        """Test provider assignment with no matches."""
        mock_conn.execute.return_value.fetchall.return_value = []
        
        provider = assign_provider_to_patient(
            mock_conn,
            patient_state="XX",  # Invalid state
        )
        
        assert provider is None
    
    def test_assign_facility_to_patient(self, mock_conn, sample_facility_row):
        """Test facility assignment."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        facility = assign_facility_to_patient(
            mock_conn,
            patient_state="TX",
            patient_city="Houston",
            seed=42,
        )
        
        assert facility is not None
        assert facility.state == "TX"


# =============================================================================
# Path Discovery Tests
# =============================================================================

class TestPathDiscovery:
    """Tests for database path discovery."""
    
    def test_networksim_db_path_structure(self):
        """Test that path has expected structure."""
        path = get_networksim_db_path()
        
        # Should point to main healthsim database (consolidated)
        assert path.name == "healthsim_current_backup.duckdb"
        assert "healthsim-workspace" in str(path)


# =============================================================================
# Integration Tests (require real database)
# =============================================================================

class TestIntegration:
    """Integration tests with real database.
    
    These tests require the HealthSim database to be available.
    They are skipped if the database is not found.
    """
    
    @pytest.fixture
    def real_conn(self):
        """Get connection to real database if available."""
        import duckdb
        
        db_path = get_networksim_db_path()
        if not db_path.exists():
            pytest.skip(f"HealthSim database not found: {db_path}")
        
        conn = duckdb.connect(str(db_path), read_only=True)
        yield conn
        conn.close()
    
    def test_real_provider_count(self, real_conn):
        """Test counting real providers."""
        resolver = NetworkSimResolver(real_conn)
        count = resolver.count_providers()
        
        # Should have millions of providers
        assert count > 1_000_000
    
    def test_real_facility_count(self, real_conn):
        """Test counting real facilities."""
        resolver = NetworkSimResolver(real_conn)
        count = resolver.count_facilities()
        
        # Should have tens of thousands of facilities
        assert count > 10_000
    
    def test_real_provider_search(self, real_conn):
        """Test searching real providers."""
        resolver = NetworkSimResolver(real_conn)
        providers = resolver.find_providers(
            state="TX",
            city="HOUSTON",
            limit=10,
        )
        
        assert len(providers) == 10
        for p in providers:
            assert p.practice_state == "TX"
    
    def test_real_facility_search(self, real_conn):
        """Test searching real facilities."""
        resolver = NetworkSimResolver(real_conn)
        facilities = resolver.find_facilities(
            state="CA",
            facility_type="hospital",
            limit=10,
        )
        
        assert len(facilities) <= 10
        for f in facilities:
            assert f.state == "CA"
    
    def test_real_states_list(self, real_conn):
        """Test listing real states."""
        resolver = NetworkSimResolver(real_conn)
        states = resolver.list_states_with_providers()
        
        # Should have 50+ states/territories
        assert len(states) >= 50
        
        # Texas should have many providers
        tx = next((s for s in states if s["state"] == "TX"), None)
        assert tx is not None
        assert tx["count"] > 100_000
