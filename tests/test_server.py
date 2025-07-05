"""
Module for testing the MCP server creation and tool registration.
This module contains unit tests to verify the server setup and tool functionality.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_environment_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server creation and tool registration.
    This class contains tests to ensure the server is set up correctly and tools are registered as expected.
    """
    @patch("hkopenai.hk_environment_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_environment_mcp_server.server.tool_aqhi")
    def test_create_mcp_server(self, mock_tool_aqhi, mock_fastmcp):
        """
        Test the creation of the MCP server and registration of tools.
        Verifies that the server is initialized correctly and tools are properly decorated and callable.
        Args:
            mock_tool_aqhi: Mock object for the tool_aqhi module.
            mock_fastmcp: Mock object for the FastMCP class.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 1)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 1)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_current_aqhi"]()
        mock_tool_aqhi.get_current_aqhi.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
