"""
Module for testing the AQHI tool functionality.
This module contains unit tests to verify fetching and parsing of AQHI data.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_environment_mcp_server.tool_aqhi import (
    fetch_aqhi_data,
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
        self.sample_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href='style.xsl' type='text/xsl' media='screen'?>
<rss version="2.0">
   <channel>
       <title>Environmental Protection Department - AQHI</title>
       <link>http://www.aqhi.gov.hk</link>
       <image>
           <title>Environmental Protection Department - AQHI</title>
           <link>http://www.aqhi.gov.hk</link>
           <url>/epd/ddata/html/img/logo-main.png</url>
       </image>
       <description>Environmental Protection Department - AQHI</description>
       <language>en-us</language>
       <copyright>Environmental Protection Department</copyright>
       <webMaster>enquiry@epd.gov.hk</webMaster>
       <pubDate>Tue, 17 Jun 2025 19:30:00 +0800</pubDate>
       <lastBuildDate>Tue, 17 Jun 2025 19:30:00 +0800</lastBuildDate>
       <item>
           <title>Central/Western : 2 : Low</title>
           <guid isPermaLink="true">http://www.aqhi.gov.hk/</guid>
           <link>http://www.aqhi.gov.hk</link>
           <pubDate>Tue, 17 Jun 2025 19:30:00 +0800</pubDate>
           <description>
               <![CDATA[Central/Western - General Stations: 2 Low - Tue, 17 Jun 2025 19:30]]>
           </description>
       </item>
       <item>
           <title>Southern : 2 : Low</title>
           <guid isPermaLink="true">http://www.aqhi.gov.hk/</guid>
           <link>http://www.aqhi.gov.hk</link>
           <pubDate>Tue, 17 Jun 2025 19:30:00 +0800</pubDate>
           <description>
               <![CDATA[Southern - General Stations: 2 Low - Tue, 17 Jun 2025 19:30]]>
           </description>
       </item>
   </channel>
</rss>
        """

    @patch("requests.get")
    def test_fetch_aqhi_data(self, mock_get):
        """
        Test fetching AQHI data from the Environmental Protection Department RSS feed.
        Verifies that the data is fetched correctly using a mocked HTTP response.
        Args:
            mock_get: Mock object for the requests.get function.
        """
        mock_response = Mock()
        mock_response.text = self.sample_xml
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_aqhi_data()
        self.assertEqual(result, self.sample_xml)
        mock_get.assert_called_once_with(
            "https://www.aqhi.gov.hk/epd/ddata/html/out/aqhi_ind_rss_Eng.xml"
        )

    def test_parse_aqhi_data(self):
        """
        Test parsing of AQHI XML data to extract air quality information.
        Verifies that the XML data is correctly parsed into a list of dictionaries.
        """
        result = parse_aqhi_data(self.sample_xml)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station"], "Central/Western")
        self.assertEqual(result[0]["aqhi_value"], "2")
        self.assertEqual(result[0]["risk_level"], "Low")
        self.assertEqual(result[0]["station_type"], "General Stations")
        self.assertEqual(result[1]["station"], "Southern")
        self.assertEqual(result[1]["aqhi_value"], "2")
        self.assertEqual(result[1]["risk_level"], "Low")
        self.assertEqual(result[1]["station_type"], "General Stations")

    @patch("hkopenai.hk_environment_mcp_server.tool_aqhi.fetch_aqhi_data")
    def test_get_current_aqhi(self, mock_fetch):
        """
        Test retrieval of current AQHI data for monitoring stations.
        Verifies that the function fetches and parses data correctly using a mocked fetch operation.
        Args:
            mock_fetch: Mock object for the fetch_aqhi_data function.
        """
        mock_fetch.return_value = self.sample_xml

        result = _get_current_aqhi()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station"], "Central/Western")
        mock_fetch.assert_called_once()

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
            "hkopenai.hk_environment_mcp_server.tool_aqhi._get_current_aqhi"
        ) as mock_get_current_aqhi:
            decorated_function()
            mock_get_current_aqhi.assert_called_once()


class TestAQHITool(unittest.TestCase):
    """
    Test class for verifying AQHI tool functionality.
    This class contains tests to ensure correct fetching and parsing of AQHI data from the Environmental Protection Department.
    """

    def setUp(self):
        self.sample_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href='style.xsl' type='text/xsl' media='screen'?>
<rss version="2.0">
   <channel>
       <title>Environmental Protection Department - AQHI</title>
       <link>http://www.aqhi.gov.hk</link>
       <image>
           <title>Environmental Protection Department - AQHI</title>
           <link>http://www.aqhi.gov.hk</link>
           <url>/epd/ddata/html/img/logo-main.png</url>
       </image>
       <description>Environmental Protection Department - AQHI</description>
       <language>en-us</language>
       <copyright>Environmental Protection Department</copyright>
       <webMaster>enquiry@epd.gov.hk</webMaster>
       <pubDate>Tue, 17 Jun 2025 19:30:00 +0800</pubDate>
       <lastBuildDate>Tue, 17 Jun 2025 19:30:00 +0800</lastBuildDate>
       <item>
           <title>Central/Western : 2 : Low</title>
           <guid isPermaLink="true">http://www.aqhi.gov.hk/</guid>
           <link>http://www.aqhi.gov.hk</link>
           <pubDate>Tue, 17 Jun 2025 19:30:00 +0800</pubDate>
           <description>
               <![CDATA[Central/Western - General Stations: 2 Low - Tue, 17 Jun 2025 19:30]]>
           </description>
       </item>
       <item>
           <title>Southern : 2 : Low</title>
           <guid isPermaLink="true">http://www.aqhi.gov.hk/</guid>
           <link>http://www.aqhi.gov.hk</link>
           <pubDate>Tue, 17 Jun 2025 19:30:00 +0800</pubDate>
           <description>
               <![CDATA[Southern - General Stations: 2 Low - Tue, 17 Jun 2025 19:30]]>
           </description>
       </item>
   </channel>
</rss>
        """

    @patch("requests.get")
    def test_fetch_aqhi_data(self, mock_get):
        """
        Test fetching AQHI data from the Environmental Protection Department RSS feed.
        Verifies that the data is fetched correctly using a mocked HTTP response.
        Args:
            mock_get: Mock object for the requests.get function.
        """
        mock_response = Mock()
        mock_response.text = self.sample_xml
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_aqhi_data()
        self.assertEqual(result, self.sample_xml)
        mock_get.assert_called_once_with(
            "https://www.aqhi.gov.hk/epd/ddata/html/out/aqhi_ind_rss_Eng.xml"
        )

    def test_parse_aqhi_data(self):
        """
        Test parsing of AQHI XML data to extract air quality information.
        Verifies that the XML data is correctly parsed into a list of dictionaries.
        """
        result = parse_aqhi_data(self.sample_xml)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station"], "Central/Western")
        self.assertEqual(result[0]["aqhi_value"], "2")
        self.assertEqual(result[0]["risk_level"], "Low")
        self.assertEqual(result[0]["station_type"], "General Stations")
        self.assertEqual(result[1]["station"], "Southern")
        self.assertEqual(result[1]["aqhi_value"], "2")
        self.assertEqual(result[1]["risk_level"], "Low")
        self.assertEqual(result[1]["station_type"], "General Stations")

    @patch("hkopenai.hk_environment_mcp_server.tool_aqhi.fetch_aqhi_data")
    def test_get_current_aqhi(self, mock_fetch):
        """
        Test retrieval of current AQHI data for monitoring stations.
        Verifies that the function fetches and parses data correctly using a mocked fetch operation.
        Args:
            mock_fetch: Mock object for the fetch_aqhi_data function.
        """
        mock_fetch.return_value = self.sample_xml

        result = _get_current_aqhi()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station"], "Central/Western")
        mock_fetch.assert_called_once()

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
            "hkopenai.hk_environment_mcp_server.tool_aqhi._get_current_aqhi"
        ) as mock_get_current_aqhi:
            decorated_function()
            mock_get_current_aqhi.assert_called_once()


if __name__ == "__main__":
    unittest.main()
