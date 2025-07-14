"""
Module for fetching and parsing Air Quality Health Index (AQHI) data from the Environmental Protection Department in Hong Kong.
This module provides functionality to retrieve current AQHI values for various monitoring stations.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict
import requests


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


def fetch_aqhi_data() -> str:
    """Fetch AQHI data from Environmental Protection Department RSS feed"""
    url = "https://www.aqhi.gov.hk/epd/ddata/html/out/aqhi_ind_rss_Eng.xml"
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_aqhi_data(xml_data: str) -> List[Dict]:
    """Parse AQHI XML data to extract air quality information for each station

    Args:
        xml_data: Raw XML string from the AQHI RSS feed

    Returns:
        List of dictionaries containing AQHI data for each station
    """
    # Clean the XML data by removing any leading BOM or whitespace
    xml_data = xml_data.strip()
    if xml_data.startswith("\ufeff"):
        xml_data = xml_data[1:]
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")
    aqhi_data = []

    for item in items:
        title_elem = item.find("title")
        desc_elem = item.find("description")

        if title_elem is None or desc_elem is None:
            continue

        title = title_elem.text
        description = desc_elem.text

        if title is None or description is None:
            continue

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


def _get_current_aqhi() -> List[Dict]:
    """Get current Air Quality Health Index (AQHI) at individual general and roadside Air Quality Monitoring stations in Hong Kong

    Returns:
        List of dictionaries with AQHI data including station name, AQHI value, risk level, and station type
    """
    xml_data = fetch_aqhi_data()
    return parse_aqhi_data(xml_data)
