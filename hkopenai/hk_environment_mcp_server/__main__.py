"""
Main entry point for the HK OpenAI Environment MCP Server.
This module initiates the server application when run as a script.
"""



from hkopenai_common.cli_utils import cli_main
from .server import server

if __name__ == "__main__":
    cli_main(server, "HK Environment MCP Server")
