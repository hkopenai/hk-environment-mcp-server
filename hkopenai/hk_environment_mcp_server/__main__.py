"""
Console-script entry point for hkopenai.hk_environment_mcp_server.
"""

from hkopenai_common.cli_utils import cli_main
from .server import server


def main():
    """Console-script entry point for the hk environment mcp server."""
    cli_main(server, "hk environment mcp server")


if __name__ == "__main__":
    main()
