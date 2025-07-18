"""
Module for setting up and running the HK OpenAI Environment MCP Server.
This server provides tools and resources related to environmental data in Hong Kong.
"""

from fastmcp import FastMCP
from .tools import aqhi


def server():
    """
    Create and configure the MCP server for HK OpenAI Environment.
    This function initializes the server with necessary tools and configurations.

    Returns:
        FastMCP: Configured MCP server instance.
    """
    mcp = FastMCP(name="HK OpenAI environment Server")

    aqhi.register(mcp)

    return mcp
