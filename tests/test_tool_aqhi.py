import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_environment_mcp_server import tool_aqhi


class TestAQHITool(unittest.TestCase):
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
        mock_response = Mock()
        mock_response.text = self.sample_xml
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = tool_aqhi.fetch_aqhi_data()
        self.assertEqual(result, self.sample_xml)
        mock_get.assert_called_once_with(
            "https://www.aqhi.gov.hk/epd/ddata/html/out/aqhi_ind_rss_Eng.xml"
        )

    def test_parse_aqhi_data(self):
        result = tool_aqhi.parse_aqhi_data(self.sample_xml)
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
        mock_fetch.return_value = self.sample_xml

        result = tool_aqhi.get_current_aqhi()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station"], "Central/Western")
        mock_fetch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
