"""
HealthSim MCP Server.

Provides MCP tools for interacting with the HealthSim DuckDB database.
This server is the single connection holder, solving the DuckDB file locking issue.

Tools provided:
- healthsim_list_scenarios: List all saved scenarios
- healthsim_load_scenario: Load a scenario by name/ID
- healthsim_save_scenario: Save a new scenario
- healthsim_delete_scenario: Delete a scenario
- healthsim_query: Execute read-only SQL queries
- healthsim_get_summary: Get token-efficient scenario summary
- healthsim_query_reference: Query PopulationSim reference data

Usage:
    python healthsim_mcp.py
    
Configuration in claude_desktop_config.json:
    "healthsim-mcp": {
        "command": "python",
        "args": ["/path/to/healthsim_mcp.py"]
    }
"""

import json
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

# Add healthsim to path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))

from healthsim.db import get_connection, DatabaseConnection
from healthsim.state import StateManager


# =============================================================================
# Lifespan Management - Single Database Connection
# =============================================================================

@asynccontextmanager
async def app_lifespan(app):
    """Manage the single DuckDB connection for the server's lifetime."""
    # Initialize connection and state manager
    conn = get_connection()
    manager = StateManager(connection=conn)
    
    yield {"conn": conn, "manager": manager}
    
    # Cleanup on shutdown
    DatabaseConnection.reset()


# Initialize the MCP server with lifespan
mcp = FastMCP("healthsim_mcp", lifespan=app_lifespan)


# =============================================================================
# Pydantic Input Models
# =============================================================================

class ListScenariosInput(BaseModel):
    """Input for listing scenarios."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    tag: Optional[str] = Field(default=None, description="Filter by tag")
    search: Optional[str] = Field(default=None, description="Search in name/description")
    limit: int = Field(default=50, description="Maximum results", ge=1, le=200)


class LoadScenarioInput(BaseModel):
    """Input for loading a scenario."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name_or_id: str = Field(..., description="Scenario name or UUID", min_length=1)
    include_entities: bool = Field(default=True, description="Include full entity data")


class SaveScenarioInput(BaseModel):
    """Input for saving a scenario."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str = Field(..., description="Unique scenario name", min_length=1, max_length=200)
    entities: Dict[str, List[Dict[str, Any]]] = Field(..., description="Entity dict: {type: [entities]}")
    description: Optional[str] = Field(default=None, description="Scenario description")
    tags: Optional[List[str]] = Field(default=None, description="Tags for filtering")
    overwrite: bool = Field(default=False, description="Overwrite if exists")


class DeleteScenarioInput(BaseModel):
    """Input for deleting a scenario."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name_or_id: str = Field(..., description="Scenario name or UUID", min_length=1)
    confirm: bool = Field(default=False, description="Must be True to delete")


class QueryInput(BaseModel):
    """Input for SQL queries."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    sql: str = Field(..., description="SQL query (SELECT only)", min_length=1)
    limit: int = Field(default=100, description="Max rows to return", ge=1, le=1000)


class GetSummaryInput(BaseModel):
    """Input for getting scenario summary."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    scenario_id_or_name: str = Field(..., description="Scenario name or UUID", min_length=1)
    include_samples: bool = Field(default=True, description="Include sample entities")
    samples_per_type: int = Field(default=3, description="Samples per entity type", ge=1, le=10)


class QueryReferenceInput(BaseModel):
    """Input for querying reference data."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    table: str = Field(..., description="Reference table: places_county, places_tract, svi_county, svi_tract, adi_blockgroup")
    state: Optional[str] = Field(default=None, description="Filter by state abbreviation (e.g., 'CA')")
    county: Optional[str] = Field(default=None, description="Filter by county name")
    limit: int = Field(default=20, description="Max rows", ge=1, le=100)


# =============================================================================
# Tool Implementations
# =============================================================================

@mcp.tool(
    name="healthsim_list_scenarios",
    annotations={
        "title": "List HealthSim Scenarios",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
async def list_scenarios(params: ListScenariosInput) -> str:
    """List all saved scenarios in the HealthSim database.
    
    Returns scenario names, descriptions, entity counts, and tags.
    Use this to discover available scenarios before loading them.
    
    Returns:
        JSON list of scenario summaries with: scenario_id, name, description,
        created_at, updated_at, entity_count, tags
    """
    from mcp.server.fastmcp import Context
    ctx = mcp.get_context()
    manager = ctx.request_context.lifespan_state["manager"]
    
    scenarios = manager.list_scenarios(
        tag=params.tag,
        search=params.search,
        limit=params.limit,
    )
    
    # Format for readability
    result = []
    for s in scenarios:
        result.append({
            "scenario_id": s["scenario_id"],
            "name": s["name"],
            "description": s.get("description"),
            "entity_count": s.get("entity_count", 0),
            "tags": s.get("tags", []),
            "created_at": str(s.get("created_at", "")),
            "updated_at": str(s.get("updated_at", "")),
        })
    
    return json.dumps(result, indent=2, default=str)


@mcp.tool(
    name="healthsim_load_scenario",
    annotations={
        "title": "Load HealthSim Scenario",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
async def load_scenario(params: LoadScenarioInput) -> str:
    """Load a scenario by name or ID.
    
    Returns full scenario data including all entities. For large scenarios,
    consider using healthsim_get_summary instead for a token-efficient summary.
    
    Returns:
        JSON with scenario metadata and entities dict
    """
    ctx = mcp.get_context()
    manager = ctx.request_context.lifespan_state["manager"]
    
    try:
        scenario = manager.load_scenario(params.name_or_id)
        
        if not params.include_entities:
            # Return metadata only
            scenario.pop("entities", None)
        
        return json.dumps(scenario, indent=2, default=str)
    except ValueError as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_save_scenario",
    annotations={
        "title": "Save HealthSim Scenario",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
    }
)
async def save_scenario(params: SaveScenarioInput) -> str:
    """Save a scenario to the HealthSim database.
    
    Entities should be a dict mapping entity type to list of entities:
    {
        "patients": [{...}, {...}],
        "encounters": [{...}],
        "claims": [{...}]
    }
    
    Supported entity types: patients, members, encounters, claims, 
    claim_lines, prescriptions, subjects, etc.
    
    Returns:
        JSON with scenario_id and status
    """
    ctx = mcp.get_context()
    manager = ctx.request_context.lifespan_state["manager"]
    
    try:
        scenario_id = manager.save_scenario(
            name=params.name,
            entities=params.entities,
            description=params.description,
            tags=params.tags,
            overwrite=params.overwrite,
        )
        
        # Get entity counts
        entity_counts = {k: len(v) for k, v in params.entities.items()}
        
        return json.dumps({
            "status": "saved",
            "scenario_id": scenario_id,
            "name": params.name,
            "entity_counts": entity_counts,
            "total_entities": sum(entity_counts.values()),
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_delete_scenario",
    annotations={
        "title": "Delete HealthSim Scenario",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
    }
)
async def delete_scenario(params: DeleteScenarioInput) -> str:
    """Delete a scenario from the database.
    
    CAUTION: This permanently removes the scenario and all linked entities.
    You must set confirm=True to actually delete.
    
    Returns:
        JSON with deletion status
    """
    ctx = mcp.get_context()
    manager = ctx.request_context.lifespan_state["manager"]
    
    if not params.confirm:
        return json.dumps({
            "error": "Must set confirm=True to delete. This action is permanent.",
            "scenario": params.name_or_id,
        })
    
    try:
        deleted = manager.delete_scenario(params.name_or_id, confirm=True)
        return json.dumps({
            "status": "deleted" if deleted else "not_found",
            "scenario": params.name_or_id,
        })
    except ValueError as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_query",
    annotations={
        "title": "Query HealthSim Database",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
async def query(params: QueryInput) -> str:
    """Execute a SQL query against the HealthSim database.
    
    Only SELECT queries are allowed. Use this for:
    - Exploring reference data (ref_places_county, ref_svi_tract, etc.)
    - Querying entity tables (patients, members, encounters, claims)
    - Running analytics queries
    
    Available tables: SHOW TABLES for full list.
    
    Returns:
        JSON with columns and rows
    """
    ctx = mcp.get_context()
    conn = ctx.request_context.lifespan_state["conn"]
    
    # Basic SQL injection protection
    sql_lower = params.sql.lower().strip()
    if not sql_lower.startswith(("select", "show", "describe", "with")):
        return json.dumps({
            "error": "Only SELECT, SHOW, DESCRIBE, and WITH queries are allowed",
        })
    
    # Check for dangerous keywords
    dangerous = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    for keyword in dangerous:
        if keyword in sql_lower.split():
            return json.dumps({
                "error": f"Query contains forbidden keyword: {keyword}",
            })
    
    try:
        # Add LIMIT if not present
        if "limit" not in sql_lower:
            sql = f"{params.sql.rstrip(';')} LIMIT {params.limit}"
        else:
            sql = params.sql
        
        result = conn.execute(sql).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        # Convert to list of dicts
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "columns": columns,
            "row_count": len(rows),
            "rows": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_get_summary",
    annotations={
        "title": "Get Scenario Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
async def get_summary(params: GetSummaryInput) -> str:
    """Get a token-efficient summary of a scenario.
    
    Use this instead of load_scenario when you need context about a scenario
    without loading all entities (~500 tokens vs potentially 10K+).
    
    Returns:
        JSON with entity counts, statistics, and optional samples
    """
    ctx = mcp.get_context()
    manager = ctx.request_context.lifespan_state["manager"]
    
    try:
        summary = manager.get_summary(
            params.scenario_id_or_name,
            include_samples=params.include_samples,
            samples_per_type=params.samples_per_type,
        )
        
        # Convert to dict for JSON serialization
        return json.dumps(summary.to_dict(), indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_query_reference",
    annotations={
        "title": "Query Reference Data",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
async def query_reference(params: QueryReferenceInput) -> str:
    """Query PopulationSim reference data tables.
    
    Available tables:
    - places_county: CDC PLACES county-level health indicators (3,143 rows)
    - places_tract: CDC PLACES tract-level health indicators (83,522 rows)
    - svi_county: Social Vulnerability Index by county (3,144 rows)
    - svi_tract: Social Vulnerability Index by tract (84,120 rows)
    - adi_blockgroup: Area Deprivation Index by block group (242,336 rows)
    
    Returns:
        JSON with columns and filtered rows
    """
    ctx = mcp.get_context()
    conn = ctx.request_context.lifespan_state["conn"]
    
    # Map short names to full table names
    table_map = {
        "places_county": "ref_places_county",
        "places_tract": "ref_places_tract",
        "svi_county": "ref_svi_county",
        "svi_tract": "ref_svi_tract",
        "adi_blockgroup": "ref_adi_blockgroup",
    }
    
    table = table_map.get(params.table)
    if not table:
        return json.dumps({
            "error": f"Unknown table: {params.table}",
            "available": list(table_map.keys()),
        })
    
    # Build query with filters
    conditions = []
    query_params = []
    
    if params.state:
        conditions.append("stateabbr = ?")
        query_params.append(params.state.upper())
    
    if params.county:
        conditions.append("countyname ILIKE ?")
        query_params.append(f"%{params.county}%")
    
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    sql = f"SELECT * FROM {table}{where_clause} LIMIT {params.limit}"
    
    try:
        result = conn.execute(sql, query_params).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "table": table,
            "columns": columns,
            "row_count": len(rows),
            "rows": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_tables",
    annotations={
        "title": "List Database Tables",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
async def list_tables() -> str:
    """List all tables in the HealthSim database.
    
    Returns table names grouped by category:
    - Reference tables (ref_*): PopulationSim demographic/health data
    - Entity tables: patients, members, encounters, claims, etc.
    - System tables: scenarios, scenario_entities, schema_migrations
    
    Returns:
        JSON with categorized table names
    """
    ctx = mcp.get_context()
    conn = ctx.request_context.lifespan_state["conn"]
    
    result = conn.execute("SHOW TABLES").fetchall()
    tables = [row[0] for row in result]
    
    # Categorize
    reference = [t for t in tables if t.startswith("ref_")]
    system = ["scenarios", "scenario_entities", "scenario_tags", "schema_migrations"]
    entity = [t for t in tables if t not in reference and t not in system]
    
    return json.dumps({
        "reference_tables": reference,
        "entity_tables": entity,
        "system_tables": [t for t in system if t in tables],
        "total": len(tables),
    }, indent=2)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    mcp.run()
