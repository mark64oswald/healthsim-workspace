"""Tests for reference profile resolver."""

import pytest
import duckdb

from healthsim.generation.reference_profiles import (
    DemographicProfile,
    GeographyLevel,
    GeographyReference,
    ReferenceProfileResolver,
    create_hybrid_profile,
    list_counties,
    list_states,
    merge_profile_with_reference,
    resolve_geography,
)


@pytest.fixture
def conn():
    """Create test database connection."""
    # Use the actual healthsim database with imported reference data
    return duckdb.connect('/Users/markoswald/Developer/projects/healthsim-workspace/healthsim_current.duckdb')


class TestGeographyReference:
    """Tests for GeographyReference dataclass."""
    
    def test_creation(self):
        """Test creating a geography reference."""
        ref = GeographyReference(
            level=GeographyLevel.COUNTY,
            code="48201",
            name="Harris County"
        )
        assert ref.level == GeographyLevel.COUNTY
        assert ref.code == "48201"
        assert ref.name == "Harris County"
    
    def test_state_level(self):
        """Test state-level reference."""
        ref = GeographyReference(
            level=GeographyLevel.STATE,
            code="TX"
        )
        assert ref.level == GeographyLevel.STATE


class TestDemographicProfile:
    """Tests for DemographicProfile dataclass."""
    
    def test_creation(self):
        """Test creating a demographic profile."""
        profile = DemographicProfile(
            geography=GeographyReference(GeographyLevel.COUNTY, "48201"),
            population=4835125,
            pct_diabetes=13.2
        )
        assert profile.population == 4835125
        assert profile.pct_diabetes == 13.2


class TestReferenceProfileResolver:
    """Tests for ReferenceProfileResolver."""
    
    def test_creation(self, conn):
        """Test creating a resolver."""
        resolver = ReferenceProfileResolver(conn)
        assert resolver.conn is not None
    
    def test_resolve_county_harris(self, conn):
        """Test resolving Harris County TX."""
        resolver = ReferenceProfileResolver(conn)
        profile = resolver.resolve_county("48201")
        
        assert profile.geography.level == GeographyLevel.COUNTY
        assert profile.geography.code == "48201"
        assert profile.population > 4000000  # Harris is large
        assert profile.pct_diabetes > 0
        assert profile.pct_obesity > 0
        assert profile.pct_age_65_plus > 0
    
    def test_resolve_county_demographics(self, conn):
        """Test that county demographics are reasonable."""
        resolver = ReferenceProfileResolver(conn)
        profile = resolver.resolve_county("48201")
        
        # Age should sum to ~100
        total_age = (profile.pct_age_under_17 + 
                     profile.pct_age_18_64 + 
                     profile.pct_age_65_plus)
        assert 99 <= total_age <= 101
        
        # Gender should sum to 100
        assert profile.pct_male + profile.pct_female == 100
    
    def test_resolve_state_texas(self, conn):
        """Test resolving Texas state."""
        resolver = ReferenceProfileResolver(conn)
        profile = resolver.resolve_state("TX")
        
        assert profile.geography.level == GeographyLevel.STATE
        assert profile.geography.code == "TX"
        assert profile.population > 20000000  # TX is large
        assert profile.pct_diabetes > 0
    
    def test_resolve_invalid_county(self, conn):
        """Test that invalid county raises error."""
        resolver = ReferenceProfileResolver(conn)
        with pytest.raises(ValueError, match="No data found"):
            resolver.resolve_county("99999")
    
    def test_to_profile_spec(self, conn):
        """Test converting profile to spec."""
        resolver = ReferenceProfileResolver(conn)
        profile = resolver.resolve_county("48201")
        spec = resolver.to_profile_spec(profile)
        
        # Check structure
        assert "profile" in spec
        assert "demographics" in spec["profile"]
        assert "clinical" in spec["profile"]
        
        # Check reference is preserved
        assert spec["profile"]["demographics"]["source"] == "populationsim"
        assert spec["profile"]["demographics"]["reference"]["code"] == "48201"
        
        # Check age bands were created
        assert "age" in spec["profile"]["demographics"]
        age_spec = spec["profile"]["demographics"]["age"]
        assert age_spec["type"] == "age_bands"
        
        # Check clinical conditions
        conditions = spec["profile"]["clinical"]["conditions"]
        diabetes_cond = next(c for c in conditions if c["code"] == "E11")
        assert diabetes_cond["prevalence"] > 0


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_resolve_geography_county(self, conn):
        """Test resolve_geography with county."""
        spec = {"type": "county", "fips": "48201"}
        profile = resolve_geography(spec, conn)
        
        assert profile.geography.level == GeographyLevel.COUNTY
        assert profile.geography.code == "48201"
    
    def test_resolve_geography_state(self, conn):
        """Test resolve_geography with state."""
        spec = {"type": "state", "code": "TX"}
        profile = resolve_geography(spec, conn)
        
        assert profile.geography.level == GeographyLevel.STATE
    
    def test_list_counties(self, conn):
        """Test listing counties."""
        counties = list_counties(conn, "TX")
        
        assert len(counties) > 200  # TX has 254 counties
        assert all("fips" in c for c in counties)
        
        # Find Harris
        harris = next(c for c in counties if c["fips"] == "48201")
        assert harris["name"] == "Harris"
    
    def test_list_states(self, conn):
        """Test listing states."""
        states = list_states(conn)
        
        assert len(states) >= 50
        tx = next(s for s in states if s["abbr"] == "TX")
        assert tx["population"] > 0
        assert tx["county_count"] >= 250  # TX has ~254 counties



class TestHybridProfiles:
    """Tests for hybrid profile support."""
    
    def test_merge_basic(self, conn):
        """Test basic merge with reference profile."""
        resolver = ReferenceProfileResolver(conn)
        ref_profile = resolver.resolve_county("48201")
        
        user_spec = {
            "profile": {
                "id": "test-hybrid",
                "generation": {"count": 100}
            }
        }
        
        merged = merge_profile_with_reference(user_spec, ref_profile)
        
        # Should have added demographics
        assert "demographics" in merged["profile"]
        assert "age" in merged["profile"]["demographics"]
        assert "gender" in merged["profile"]["demographics"]
        
        # Should have added clinical conditions
        assert "clinical" in merged["profile"]
        
        # Should have reference metadata
        assert "_reference" in merged["profile"]
    
    def test_merge_with_age_override(self, conn):
        """Test that user age spec overrides reference."""
        resolver = ReferenceProfileResolver(conn)
        ref_profile = resolver.resolve_county("48201")
        
        user_spec = {
            "profile": {
                "demographics": {
                    "age": {"type": "normal", "mean": 72, "std_dev": 8}
                }
            }
        }
        
        merged = merge_profile_with_reference(user_spec, ref_profile)
        
        # User's age override should be preserved
        assert merged["profile"]["demographics"]["age"]["type"] == "normal"
        assert merged["profile"]["demographics"]["age"]["mean"] == 72
        
        # But gender should come from reference
        assert "gender" in merged["profile"]["demographics"]
    
    def test_merge_with_clinical_override(self, conn):
        """Test that user clinical spec overrides reference."""
        resolver = ReferenceProfileResolver(conn)
        ref_profile = resolver.resolve_county("48201")
        
        user_spec = {
            "profile": {
                "clinical": {
                    "primary_condition": {"code": "E11", "prevalence": 1.0}
                }
            }
        }
        
        merged = merge_profile_with_reference(user_spec, ref_profile)
        
        # User's clinical should be preserved
        assert merged["profile"]["clinical"]["primary_condition"]["code"] == "E11"
        
        # Reference conditions should NOT be added since user specified clinical
        assert "conditions" not in merged["profile"]["clinical"]
    
    def test_create_hybrid_profile(self, conn):
        """Test create_hybrid_profile convenience function."""
        spec = {
            "profile": {
                "id": "harris-test",
                "generation": {"count": 50},
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"}
                }
            }
        }
        
        hybrid = create_hybrid_profile(spec, conn)
        
        # Should have demographics from PopulationSim
        assert "age" in hybrid["profile"]["demographics"]
        assert "gender" in hybrid["profile"]["demographics"]
        
        # Should have reference metadata
        assert hybrid["profile"]["_reference"]["geography"]["code"] == "48201"
    
    def test_create_hybrid_with_state(self, conn):
        """Test create_hybrid_profile with state reference."""
        spec = {
            "profile": {
                "id": "texas-test",
                "generation": {"count": 100},
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "state", "code": "TX"}
                }
            }
        }
        
        hybrid = create_hybrid_profile(spec, conn)
        
        assert hybrid["profile"]["_reference"]["geography"]["code"] == "TX"
        assert hybrid["profile"]["_reference"]["geography"]["level"] == "state"
    
    def test_no_reference_passthrough(self, conn):
        """Test that spec without reference passes through."""
        spec = {
            "profile": {
                "id": "manual-test",
                "demographics": {
                    "age": {"type": "normal", "mean": 50, "std_dev": 10}
                }
            }
        }
        
        result = create_hybrid_profile(spec, conn)
        
        # Should be unchanged
        assert result == spec
