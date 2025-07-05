"""
Module for setting up and running the HK OpenAI Environment MCP Server.
This server provides tools and resources related to environmental data in Hong Kong.
"""

import argparse
from fastmcp import FastMCP
from hkopenai.hk_environment_mcp_server import tool_aqhi
from typing import Dict, List, Annotated, Optional
from pydantic import Field


def create_mcp_server():
    """
    Create and configure the MCP server for HK OpenAI Environment.
    This function initializes the server with necessary tools and configurations.
    
    Returns:
        FastMCP: Configured MCP server instance.
    """
    mcp = FastMCP(name="HK OpenAI environment Server")

    @mcp.tool(
        description="Current Air Quality Health Index (AQHI) at individual general and roadside Air Quality Monitoring stations in Hong Kong. The AQHIs are reported on a scale of 1 to 10 and 10+ and are grouped into five AQHI health risk categories with health advice provided. "
    )
    def get_current_aqhi() -> List[Dict]:
        return tool_aqhi.get_current_aqhi()

    return mcp


def main():
    """
    Main function to run the HK OpenAI Environment MCP Server.
    Parses command line arguments and starts the server in the specified mode.
    """
    parser = argparse.ArgumentParser(description="HKO MCP Server")
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    args = parser.parse_args()

    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http")
    else:
        server.run()


if __name__ == "__main__":
    main()
