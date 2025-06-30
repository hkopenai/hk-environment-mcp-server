# Hong Kong Government Environment MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-environment-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an MCP server that provides access to Hong Kong government environment data through a FastMCP interface. 
## Features

- **Air Quality Health Index (AQHI):** Retrieve current AQHI data from general and roadside air quality monitoring stations across Hong Kong. The AQHI is reported on a scale of 1 to 10 and 10+, grouped into five health risk categories with corresponding health advice.

## Data Source

- **Hong Kong Environmental Protection Department (EPD):** For AQHI and other environmental data.

## Prompt Examples

Here are some example prompts you can use to interact with this MCP server through Cline or other compatible interfaces:

- **AQHI Data:** "What is the current Air Quality Health Index in Hong Kong?"

## Setup

1. Clone this repository to your local machine.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

### Running Options

- **Default stdio mode:** `python server.py`
- **SSE mode (port 8000):** `python server.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hk-environment": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "uvx",
    "args": [
      "hkopenai.hk-environment-mcp-server"
    ]
  }
}
```

This configuration allows Cline to communicate with the server and utilize its tools for data retrieval.

## Testing

Tests are available in the `tests/` directory. Run with:
```bash
pytest
```
