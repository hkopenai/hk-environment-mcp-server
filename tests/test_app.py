import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_environment_mcp_server.app import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_environment_mcp_server.app.FastMCP')
    @patch('hkopenai.hk_environment_mcp_server.tool_aqhi.get_current_aqhi')
    def test_create_mcp_server(self, mock_tool_aqhi, mock_fastmcp):
        # Setup mocks
        mock_server = unittest.mock.Mock()
        
        # Track decorator calls and capture decorated functions
        decorator_calls = []
        decorated_funcs = []
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                decorated_funcs.append(f)
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_fastmcp.return_value = mock_server
        mock_tool_aqhi.return_value = [{'station': 'Central/Western', 'aqhi_value': '2', 'risk_level': 'Low', 'station_type': 'General Stations'}]

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tools were decorated
        self.assertGreaterEqual(len(decorated_funcs), 1)

if __name__ == "__main__":
    unittest.main()
