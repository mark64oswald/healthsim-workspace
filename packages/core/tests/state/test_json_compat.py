"""Tests for JSON export/import compatibility."""

import pytest
import json
from pathlib import Path
import tempfile

from healthsim.db import DatabaseConnection
from healthsim.state.manager import StateManager, reset_manager


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_json_compat.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def state_manager(test_db):
    """Create state manager with test database."""
    manager = StateManager(connection=test_db)
    yield manager
    reset_manager()


@pytest.fixture
def sample_entities():
    """Sample entities for testing."""
    return {
        'patients': [{
            'patient_id': '123e4567-e89b-12d3-a456-426614174000',
            'given_name': 'Test',
            'family_name': 'Patient',
            'date_of_birth': '1980-05-15',
            'gender': 'female',
            'ssn': '123-45-6789',
        }],
        'encounters': [{
            'encounter_id': '223e4567-e89b-12d3-a456-426614174001',
            'patient_id': '123e4567-e89b-12d3-a456-426614174000',
            'encounter_type': 'outpatient',
            'admit_datetime': '2024-01-15T10:00:00',
            'facility_name': 'Test Clinic',
        }]
    }


class TestExportToJson:
    """Tests for JSON export functionality."""
    
    def test_export_creates_file(self, state_manager, sample_entities, tmp_path):
        """Export creates a valid JSON file."""
        state_manager.save_scenario('export-test', sample_entities)
        
        output_path = tmp_path / "exported.json"
        result_path = state_manager.export_to_json('export-test', output_path)
        
        assert result_path.exists()
        assert result_path == output_path
    
    def test_export_valid_json(self, state_manager, sample_entities, tmp_path):
        """Exported file contains valid JSON."""
        state_manager.save_scenario('export-test', sample_entities)
        
        output_path = tmp_path / "exported.json"
        state_manager.export_to_json('export-test', output_path)
        
        with open(output_path) as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
        assert 'name' in data
        assert 'entities' in data
    
    def test_export_preserves_name(self, state_manager, sample_entities, tmp_path):
        """Exported JSON includes scenario name."""
        state_manager.save_scenario('my-scenario', sample_entities)
        
        output_path = tmp_path / "exported.json"
        state_manager.export_to_json('my-scenario', output_path)
        
        with open(output_path) as f:
            data = json.load(f)
        
        assert data['name'] == 'my-scenario'
    
    def test_export_preserves_entities(self, state_manager, sample_entities, tmp_path):
        """Exported JSON includes all entities."""
        state_manager.save_scenario('entity-test', sample_entities)
        
        output_path = tmp_path / "exported.json"
        state_manager.export_to_json('entity-test', output_path)
        
        with open(output_path) as f:
            data = json.load(f)
        
        assert 'patients' in data['entities']
        assert len(data['entities']['patients']) == 1
        assert data['entities']['patients'][0]['given_name'] == 'Test'
        
        assert 'encounters' in data['entities']
        assert len(data['entities']['encounters']) == 1
    
    def test_export_default_path(self, state_manager, sample_entities):
        """Export uses Downloads folder by default."""
        state_manager.save_scenario('default-path-test', sample_entities)
        
        result_path = state_manager.export_to_json('default-path-test')
        
        try:
            assert result_path.exists()
            assert result_path.parent == Path.home() / "Downloads"
            assert 'default-path-test' in result_path.name
        finally:
            # Clean up
            if result_path.exists():
                result_path.unlink()
    
    def test_export_by_id(self, state_manager, sample_entities, tmp_path):
        """Can export by scenario ID."""
        scenario_id = state_manager.save_scenario('id-export-test', sample_entities)
        
        output_path = tmp_path / "exported.json"
        result_path = state_manager.export_to_json(scenario_id, output_path)
        
        assert result_path.exists()


class TestImportFromJson:
    """Tests for JSON import functionality."""
    
    def test_import_creates_scenario(self, state_manager, tmp_path):
        """Import creates a new scenario."""
        json_data = {
            'name': 'imported-scenario',
            'description': 'Test import',
            'entities': {
                'patients': [{
                    'patient_id': '333e4567-e89b-12d3-a456-426614174002',
                    'given_name': 'Imported',
                    'family_name': 'Patient'
                }]
            }
        }
        
        json_path = tmp_path / "import-test.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        
        assert state_manager.scenario_exists(scenario_id)
    
    def test_import_preserves_name(self, state_manager, tmp_path):
        """Import uses embedded name."""
        json_data = {
            'name': 'embedded-name',
            'entities': {'patients': []}
        }
        
        json_path = tmp_path / "different-filename.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        loaded = state_manager.load_scenario(scenario_id)
        
        assert loaded['name'] == 'embedded-name'
    
    def test_import_name_override(self, state_manager, tmp_path):
        """Import can override name."""
        json_data = {
            'name': 'original-name',
            'entities': {'patients': []}
        }
        
        json_path = tmp_path / "test.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path, name='override-name')
        loaded = state_manager.load_scenario(scenario_id)
        
        assert loaded['name'] == 'override-name'
    
    def test_import_uses_filename_if_no_name(self, state_manager, tmp_path):
        """Import uses filename if no embedded name."""
        json_data = {
            'entities': {'patients': []}
        }
        
        json_path = tmp_path / "my-scenario-file.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        loaded = state_manager.load_scenario(scenario_id)
        
        assert loaded['name'] == 'my-scenario-file'
    
    def test_import_preserves_entities(self, state_manager, tmp_path):
        """Import preserves all entity data."""
        json_data = {
            'name': 'entity-import-test',
            'entities': {
                'patients': [{
                    'patient_id': 'pat-001',
                    'given_name': 'Alice',
                    'family_name': 'Smith',
                    'date_of_birth': '1990-03-15'
                }],
                'encounters': [{
                    'encounter_id': 'enc-001',
                    'patient_id': 'pat-001',
                    'encounter_type': 'inpatient'
                }]
            }
        }
        
        json_path = tmp_path / "entities.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        loaded = state_manager.load_scenario(scenario_id)
        
        assert len(loaded['entities']['patients']) == 1
        assert loaded['entities']['patients'][0]['given_name'] == 'Alice'
        assert len(loaded['entities']['encounters']) == 1
    
    def test_import_preserves_tags(self, state_manager, tmp_path):
        """Import preserves tags."""
        json_data = {
            'name': 'tagged-scenario',
            'tags': ['test', 'diabetes', 'chronic'],
            'entities': {'patients': []}
        }
        
        json_path = tmp_path / "tagged.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        tags = state_manager.get_scenario_tags(scenario_id)
        
        assert 'test' in tags
        assert 'diabetes' in tags
        assert 'chronic' in tags
    
    def test_import_with_overwrite(self, state_manager, tmp_path):
        """Import can overwrite existing scenario."""
        # Create initial scenario
        state_manager.save_scenario('overwrite-test', {'patients': [{'given_name': 'Original'}]})
        
        # Import with same name
        json_data = {
            'name': 'overwrite-test',
            'entities': {'patients': [{'given_name': 'Replacement'}]}
        }
        
        json_path = tmp_path / "overwrite.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        scenario_id = state_manager.import_from_json(json_path, overwrite=True)
        loaded = state_manager.load_scenario(scenario_id)
        
        assert loaded['entities']['patients'][0]['given_name'] == 'Replacement'


class TestLegacyFormat:
    """Tests for legacy JSON format compatibility."""
    
    def test_import_entities_at_top_level(self, state_manager, tmp_path):
        """Import handles old format with entities at top level."""
        legacy_json = {
            'name': 'legacy-scenario',
            'patients': [{'given_name': 'Legacy', 'family_name': 'Patient'}],
            'encounters': [{'encounter_type': 'outpatient'}]
        }
        
        json_path = tmp_path / "legacy.json"
        with open(json_path, 'w') as f:
            json.dump(legacy_json, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        loaded = state_manager.load_scenario(scenario_id)
        
        assert 'patients' in loaded['entities']
        assert loaded['entities']['patients'][0]['given_name'] == 'Legacy'
    
    def test_import_singular_entity_keys(self, state_manager, tmp_path):
        """Import handles singular entity keys (patient vs patients)."""
        legacy_json = {
            'name': 'singular-keys',
            'patient': [{'given_name': 'Singular'}],
            'encounter': [{'encounter_type': 'inpatient'}]
        }
        
        json_path = tmp_path / "singular.json"
        with open(json_path, 'w') as f:
            json.dump(legacy_json, f)
        
        scenario_id = state_manager.import_from_json(json_path)
        loaded = state_manager.load_scenario(scenario_id)
        
        # Should normalize to plural
        assert 'patients' in loaded['entities']
        assert loaded['entities']['patients'][0]['given_name'] == 'Singular'


class TestRoundTrip:
    """Tests for export/import round-trip."""
    
    def test_round_trip_preserves_data(self, state_manager, sample_entities, tmp_path):
        """Export then import preserves all data."""
        # Save original
        state_manager.save_scenario('round-trip-test', sample_entities)
        
        # Export
        json_path = tmp_path / "round-trip.json"
        state_manager.export_to_json('round-trip-test', json_path)
        
        # Delete original
        state_manager.delete_scenario('round-trip-test')
        
        # Import
        state_manager.import_from_json(json_path, name='round-trip-restored')
        
        # Verify
        restored = state_manager.load_scenario('round-trip-restored')
        
        assert len(restored['entities']['patients']) == 1
        assert restored['entities']['patients'][0]['given_name'] == 'Test'
        assert restored['entities']['patients'][0]['family_name'] == 'Patient'
        
        assert len(restored['entities']['encounters']) == 1
        assert restored['entities']['encounters'][0]['encounter_type'] == 'outpatient'
    
    def test_round_trip_with_tags(self, state_manager, sample_entities, tmp_path):
        """Round-trip preserves tags."""
        state_manager.save_scenario(
            'tagged-round-trip',
            sample_entities,
            tags=['important', 'test']
        )
        
        # Export and re-import
        json_path = tmp_path / "tagged.json"
        state_manager.export_to_json('tagged-round-trip', json_path)
        state_manager.delete_scenario('tagged-round-trip')
        state_manager.import_from_json(json_path)
        
        # Verify tags
        tags = state_manager.get_scenario_tags('tagged-round-trip')
        assert 'important' in tags
        assert 'test' in tags
    
    def test_round_trip_with_description(self, state_manager, sample_entities, tmp_path):
        """Round-trip preserves description."""
        state_manager.save_scenario(
            'described-round-trip',
            sample_entities,
            description='A detailed description of this scenario'
        )
        
        # Export and re-import
        json_path = tmp_path / "described.json"
        state_manager.export_to_json('described-round-trip', json_path)
        state_manager.delete_scenario('described-round-trip')
        state_manager.import_from_json(json_path)
        
        # Verify
        restored = state_manager.load_scenario('described-round-trip')
        assert restored['description'] == 'A detailed description of this scenario'
