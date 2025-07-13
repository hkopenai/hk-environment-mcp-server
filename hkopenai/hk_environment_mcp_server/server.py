"""
Module for setting up and running the HK OpenAI Environment MCP Server.
This server provides tools and resources related to environmental data in Hong Kong.
"""

from fastmcp import FastMCP
from hkopenai.hk_environment_mcp_server import tool_aqhi


def create_mcp_server():
    """
    Create and configure the MCP server for HK OpenAI Environment.
    This function initializes the server with necessary tools and configurations.
    
    Returns:
        FastMCP: Configured MCP server instance.
    """
    mcp = FastMCP(name="HK OpenAI environment Server")

    tool_aqhi.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to run the HK OpenAI Environment MCP Server.
    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
    else:
        server.run()


if __name__ == "__main__":
    main()
