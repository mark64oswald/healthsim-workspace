FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    "mcp>=1.0.0" \
    "duckdb>=0.9.0" \
    "pydantic>=2.0.0" \
    "pydantic-settings>=2.0.0" \
    "uvicorn>=0.30.0" \
    "starlette>=0.40.0" \
    "anyio>=3.5.0"

# Copy healthsim core library
COPY packages/core/src/healthsim/ /app/healthsim/

# Copy MCP server
COPY packages/mcp-server/healthsim_mcp.py /app/

# Set Python path so healthsim imports resolve
ENV PYTHONPATH=/app

# MCP server configuration — connects to MotherDuck (no local DB needed)
# MOTHERDUCK_TOKEN and HEALTHSIM_MCP_TOKEN are set via Railway env vars
ENV MCP_TRANSPORT=http
ENV MCP_PORT=8001
# HEALTHSIM_DB_PATH must be set at runtime: md:healthsim_ref?motherduck_token=<token>

EXPOSE 8001

CMD ["python", "healthsim_mcp.py"]
