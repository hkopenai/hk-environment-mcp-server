"""
Module for testing the AQHI tool functionality.
This module contains unit tests to verify fetching and parsing of AQHI data.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
import xml.etree.ElementTree as ET
import textwrap
from hkopenai_common.xml_utils import fetch_xml_from_url
from hkopenai.hk_environment_mcp_server.tools.aqhi import (
    parse_aqhi_data,
    _get_current_aqhi,
    register,
)


class TestAQHITool(unittest.TestCase):
    """
    Test class for verifying AQHI tool functionality.
    This class contains tests to ensure correct fetching and parsing of AQHI data from the Environmental Protection Department.
    """

    def setUp(self):
        self.sample_xml_dict = {
            "rss": {
                "channel": [
                    {
                        "title": ["Environmental Protection Department - AQHI"],
                        "link": ["https://www.aqhi.gov.hk"],
                        "image": [
                            {
                                "title": ["Environmental Protection Department - AQHI"],
                                "link": ["https://www.aqhi.gov.hk"],
                                "url": ["https://www.aqhi.gov.hk/common/images/logo_aqhi.svg"],
                            }
                        ],
                        "description": ["Environmental Protection Department - AQHI"],
                        "language": ["en-us"],
                        "copyright": ["Environmental Protection Department"],
                        "webMaster": ["enquiry@epd.gov.hk"],
                        "pubDate": ["Tue, 17 Jun 2025 19:30:00 +0800"],
                        "lastBuildDate": ["Tue, 17 Jun 2025 19:30:00 +0800"],
                        "item": [
                            {
                                "title": ["Central/Western : 2 : Low"],
                                "guid": ["https://www.aqhi.gov.hk/"],
                                "link": ["https://www.aqhi.gov.hk"],
                                "pubDate": ["Tue, 17 Jun 2025 19:30:00 +0800"],
                                "description": [
                                    "<![CDATA[Central/Western - General Stations: 2 Low - Tue, 17 Jun 2025 19:30]]>"
                                ],
                            },
                            {
                                "title": ["Southern : 2 : Low"],
                                "guid": ["https://www.aqhi.gov.hk/"],
                                "link": ["https://www.aqhi.gov.hk"],
                                "pubDate": ["Tue, 17 Jun 2025 19:30:00 +0800"],
                                "description": [
                                    "<![CDATA[Southern - General Stations: 2 Low - Tue, 17 Jun 2025 19:30]]>"
                                ],
                            },
                        ],
                    }
                ]
            }
        }

    def test_parse_aqhi_data(self):
        """
        Test parsing of AQHI XML data to extract air quality information.
        Verifies that the XML data is correctly parsed into a list of dictionaries.
        """
        result = parse_aqhi_data(self.sample_xml_dict)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station"], "Central/Western")
        self.assertEqual(result[0]["aqhi_value"], "2")
        self.assertEqual(result[0]["risk_level"], "Low")
        self.assertEqual(result[0]["station_type"], "General Stations")
        self.assertEqual(result[1]["station"], "Southern")
        self.assertEqual(result[1]["aqhi_value"], "2")
        self.assertEqual(result[1]["risk_level"], "Low")
        self.assertEqual(result[1]["station_type"], "General Stations")

    def test_register_tool(self):
        """
        Test the registration of the get_current_aqhi tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_current_aqhi function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Current Air Quality Health Index (AQHI) at individual general and roadside Air Quality Monitoring stations in Hong Kong. The AQHIs are reported on a scale of 1 to 10 and 10+ and are grouped into five AQHI health risk categories with health advice provided. "
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_current_aqhi")

        # Call the decorated function and verify it calls _get_current_aqhi
        with patch(
            "hkopenai.hk_environment_mcp_server.tools.aqhi._get_current_aqhi"
        ) as mock_get_current_aqhi:
            decorated_function()
            mock_get_current_aqhi.assert_called_once()

if __name__ == "__main__":
    unittest.main()