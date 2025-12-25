"""RxMemberSim MCP Server.

Implements Model Context Protocol (MCP) server for pharmacy benefit simulation.
Uses the MCP v1.x API pattern with explicit tool listing and dispatch.
"""

from datetime import date
from decimal import Decimal
import json

try:
    from mcp.server import Server
    from mcp.types import TextContent, Tool

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    Server = None  # type: ignore[misc,assignment]
    Tool = None  # type: ignore[misc,assignment]
    TextContent = None  # type: ignore[misc,assignment]

from healthsim.state import Provenance

from ..authorization.prior_auth import PriorAuthWorkflow
from ..claims.adjudication import AdjudicationEngine
from ..core.member import RxMemberFactory
from ..dur.validator import DURValidator
from ..formulary.formulary import FormularyGenerator
from ..scenarios.engine import RxScenarioEngine
from .session import session_manager

# Initialize components
member_generator = RxMemberFactory()
formulary = FormularyGenerator().generate_standard_commercial()
adjudication_engine = AdjudicationEngine(formulary=formulary)
dur_validator = DURValidator()
pa_workflow = PriorAuthWorkflow()
scenario_engine = RxScenarioEngine()

if MCP_AVAILABLE:
    server = Server("rxmembersim")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available MCP tools for RxMemberSim."""
        return [
            Tool(
                name="generate_rx_member",
                description="Generate a pharmacy benefit member with BIN, PCN, and group number",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "bin": {
                            "type": "string",
                            "description": "BIN number (identifies PBM)",
                            "default": "610014",
                        },
                        "pcn": {
                            "type": "string",
                            "description": "Processor Control Number",
                            "default": "RXTEST",
                        },
                        "group_number": {
                            "type": "string",
                            "description": "Group identifier",
                            "default": "GRP001",
                        },
                    },
                },
            ),
            Tool(
                name="check_formulary",
                description="Check formulary status and coverage tier for a drug by NDC",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "ndc": {
                            "type": "string",
                            "description": "Drug NDC to check",
                        },
                    },
                    "required": ["ndc"],
                },
            ),
            Tool(
                name="check_dur",
                description="Run Drug Utilization Review checks for potential interactions and alerts",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "gpi": {
                            "type": "string",
                            "description": "Drug GPI (Generic Product Identifier)",
                        },
                        "current_medications": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of current medication GPIs for interaction checking",
                        },
                    },
                    "required": ["gpi"],
                },
            ),
            Tool(
                name="submit_prior_auth",
                description="Submit a prior authorization request for a medication",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "member_id": {
                            "type": "string",
                            "description": "Member identifier",
                        },
                        "ndc": {
                            "type": "string",
                            "description": "Drug NDC",
                        },
                        "drug_name": {
                            "type": "string",
                            "description": "Drug name",
                        },
                        "prescriber_npi": {
                            "type": "string",
                            "description": "Prescriber NPI",
                        },
                        "prescriber_name": {
                            "type": "string",
                            "description": "Prescriber name",
                        },
                        "quantity": {
                            "type": "number",
                            "description": "Quantity requested",
                            "default": 1,
                        },
                        "days_supply": {
                            "type": "integer",
                            "description": "Days supply",
                            "default": 30,
                        },
                        "urgency": {
                            "type": "string",
                            "enum": ["routine", "urgent", "emergency"],
                            "description": "Request urgency level",
                            "default": "routine",
                        },
                    },
                    "required": ["member_id", "ndc", "drug_name", "prescriber_npi", "prescriber_name"],
                },
            ),
            Tool(
                name="run_rx_scenario",
                description="Execute a pharmacy scenario (e.g., new therapy start, refill sequence)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "scenario_id": {
                            "type": "string",
                            "description": "Scenario identifier (e.g., 'NEW_THERAPY_01')",
                        },
                        "member_id": {
                            "type": "string",
                            "description": "Optional member ID (generates new member if not provided)",
                        },
                    },
                    "required": ["scenario_id"],
                },
            ),
            Tool(
                name="list_scenarios",
                description="List available pharmacy scenarios with descriptions",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Dispatch tool calls to appropriate handlers."""
        try:
            if name == "generate_rx_member":
                result = await _generate_rx_member(**arguments)
            elif name == "check_formulary":
                result = await _check_formulary(**arguments)
            elif name == "check_dur":
                result = await _check_dur(**arguments)
            elif name == "submit_prior_auth":
                result = await _submit_prior_auth(**arguments)
            elif name == "run_rx_scenario":
                result = await _run_rx_scenario(**arguments)
            elif name == "list_scenarios":
                result = await _list_scenarios()
            else:
                result = {"error": f"Unknown tool: {name}"}

            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

    # Tool implementation functions

    async def _generate_rx_member(
        bin: str = "610014",
        pcn: str = "RXTEST",
        group_number: str = "GRP001",
    ) -> dict:
        """Generate a pharmacy benefit member."""
        member = member_generator.generate(
            bin=bin, pcn=pcn, group_number=group_number
        )
        session_manager.add_rx_member(
            rx_member=member,
            provenance=Provenance.generated(skill="generate_rx_member"),
        )
        return member.model_dump()

    async def _check_formulary(ndc: str) -> dict:
        """Check formulary status for a drug."""
        status = formulary.check_coverage(ndc)
        return status.model_dump()

    async def _check_dur(
        gpi: str,
        current_medications: list[str] | None = None,
    ) -> dict:
        """Run DUR checks for a drug."""
        result = dur_validator.validate(
            ndc="",
            gpi=gpi,
            member_id="",
            service_date=date.today(),
            current_medications=current_medications or [],
        )
        return result.model_dump()

    async def _submit_prior_auth(
        member_id: str,
        ndc: str,
        drug_name: str,
        prescriber_npi: str,
        prescriber_name: str,
        quantity: float = 1,
        days_supply: int = 30,
        urgency: str = "routine",
    ) -> dict:
        """Submit a prior authorization request."""
        request = pa_workflow.create_request(
            member_id=member_id,
            cardholder_id=member_id,
            ndc=ndc,
            drug_name=drug_name,
            quantity=Decimal(str(quantity)),
            days_supply=days_supply,
            prescriber_npi=prescriber_npi,
            prescriber_name=prescriber_name,
            urgency=urgency,
        )

        auto_response = pa_workflow.check_auto_approval(request)

        return {
            "request": request.model_dump(),
            "auto_approved": auto_response is not None,
            "response": auto_response.model_dump() if auto_response else None,
        }

    async def _run_rx_scenario(
        scenario_id: str,
        member_id: str | None = None,
    ) -> dict:
        """Execute a pharmacy scenario."""
        scenarios = {s.scenario_id: s for s in scenario_engine.list_scenarios()}

        if scenario_id not in scenarios:
            return {
                "error": f"Unknown scenario: {scenario_id}",
                "available": list(scenarios.keys()),
            }

        if not member_id:
            member = member_generator.generate()
            member_id = member.member_id

        timeline = scenario_engine.execute_scenario(
            scenario=scenarios[scenario_id],
            member_id=member_id,
        )

        return {
            "scenario": scenarios[scenario_id].model_dump(),
            "member_id": member_id,
            "events": [e.model_dump() for e in timeline.events],
        }

    async def _list_scenarios() -> list[dict]:
        """List available pharmacy scenarios."""
        return [s.model_dump() for s in scenario_engine.list_scenarios()]

    # Export functions for testing
    generate_rx_member = _generate_rx_member
    check_formulary = _check_formulary
    check_dur = _check_dur
    submit_prior_auth = _submit_prior_auth
    run_rx_scenario = _run_rx_scenario
    list_rx_scenarios = _list_scenarios

else:
    server = None
    # Stub functions when MCP not available
    async def generate_rx_member(*args, **kwargs):
        raise RuntimeError("MCP not available")
    async def check_formulary(*args, **kwargs):
        raise RuntimeError("MCP not available")
    async def check_dur(*args, **kwargs):
        raise RuntimeError("MCP not available")
    async def submit_prior_auth(*args, **kwargs):
        raise RuntimeError("MCP not available")
    async def run_rx_scenario(*args, **kwargs):
        raise RuntimeError("MCP not available")
    async def list_rx_scenarios(*args, **kwargs):
        raise RuntimeError("MCP not available")


def main() -> None:
    """Run the MCP server."""
    if not MCP_AVAILABLE:
        print("MCP package not installed. Install with: pip install mcp")
        return

    import asyncio
    from mcp.server.stdio import stdio_server

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
