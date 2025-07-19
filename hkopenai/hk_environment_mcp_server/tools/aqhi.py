"""
Module for fetching and parsing Air Quality Health Index (AQHI) data from the Environmental Protection Department in Hong Kong.
This module provides functionality to retrieve current AQHI values for various monitoring stations.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict
import requests
from hkopenai_common.xml_utils import fetch_xml_from_url


def register(mcp):
    """Registers the AQHI tool with the FastMCP server."""

    @mcp.tool(
        description="Current Air Quality Health Index (AQHI) at individual general and roadside Air Quality Monitoring stations in Hong Kong. The AQHIs are reported on a scale of 1 to 10 and 10+ and are grouped into five AQHI health risk categories with health advice provided. "
    )
    def get_current_aqhi() -> List[Dict]:
        """Get current Air Quality Health Index (AQHI) at individual general and roadside Air Quality Monitoring stations in Hong Kong

        Returns:
            List of dictionaries with AQHI data including station name, AQHI value, risk level, and station type
        """
        return _get_current_aqhi()


def parse_aqhi_data(xml_data: Dict) -> List[Dict]:
    """Parse AQHI XML data to extract air quality information for each station

    Args:
        xml_data: Dictionary from the AQHI RSS feed

    Returns:
        List of dictionaries containing AQHI data for each station
    """
    aqhi_data = []
    if "rss" in xml_data and "channel" in xml_data["rss"] and len(xml_data["rss"]["channel"]) > 0:
        channel = xml_data["rss"]["channel"][0]
        if "item" in channel:
            for item in channel["item"]:
                title = item["title"][0] if "title" in item and item["title"] else ""
                description = item["description"][0] if "description" in item and item["description"] else ""

                # Extract station name, AQHI value, and risk level from title
                title_parts = title.split(" : ")
                if len(title_parts) >= 3:
                    station = title_parts[0].strip()
                    aqhi_value = title_parts[1].strip()
                    risk_level = title_parts[2].strip()

                    # Extract station type from description
                    desc_parts = description.split(" - ")
                    station_type = "Unknown"
                    if len(desc_parts) >= 2:
                        type_info = desc_parts[1].split(":")
                        if len(type_info) >= 2:
                            station_type = type_info[0].strip()

                    aqhi_data.append(
                        {
                            "station": station,
                            "aqhi_value": aqhi_value,
                            "risk_level": risk_level,
                            "station_type": station_type,
                        }
                    )
    return aqhi_data


def _get_current_aqhi() -> List[Dict] | Dict[str, str]:
    """Get current Air Quality Health Index (AQHI) at individual general and roadside Air Quality Monitoring stations in Hong Kong

    Returns:
        List of dictionaries with AQHI data including station name, AQHI value, risk level, and station type, or an error dictionary
    """
    url = "https://www.aqhi.gov.hk/epd/ddata/html/out/aqhi_ind_rss_Eng.xml" 
    xml_data = fetch_xml_from_url(url)
    if "error" in xml_data:
        return xml_data
    return parse_aqhi_data(xml_data)
