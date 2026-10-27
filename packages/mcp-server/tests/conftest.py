"""Shared test setup for the HealthSim MCP server.

healthsim_mcp resolves its data location at import time, so isolate it from
the developer's ~/.healthsim before any test module imports the server.
"""

import os
import tempfile

if "HEALTHSIM_DB_PATH" not in os.environ:
    os.environ["HEALTHSIM_HOME"] = tempfile.mkdtemp(prefix="healthsim-test-home-")
