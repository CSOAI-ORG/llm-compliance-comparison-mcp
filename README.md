<div align="center">

# Llm Compliance Comparison MCP

**MCP server for llm compliance comparison mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-llm-compliance-comparison-mcp)](https://pypi.org/project/meok-llm-compliance-comparison-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Llm Compliance Comparison MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `compare_providers` | Compare LLM providers (Claude, GPT-4, Gemini, Llama, Mistral) against |
| `recommend_for_use_case` | Given a use case and jurisdiction, recommend the most compliant LLM provider. |
| `provider_risk_profile` | Generate a detailed risk profile for a specific LLM provider. |
| `compliance_matrix` | Generate a compliance matrix showing all providers against all frameworks. |
| `crosswalk_providers` | Map LLM provider safety policies to CSOAI Partnership Charter articles. |

## Installation

```bash
pip install meok-llm-compliance-comparison-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "llm-compliance-comparison-mcp": {
      "command": "python",
      "args": ["-m", "meok_llm_compliance_comparison_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
