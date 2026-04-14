# LLM Provider Compliance Comparison MCP Server

> **By [MEOK AI Labs](https://meok.ai)** -- Sovereign AI tools for everyone.

Compare major LLM providers (Claude, GPT-4, Gemini, Llama, Mistral) against governance standards, regulatory frameworks, and CSOAI articles. Recommend providers for specific use cases and jurisdictions. Generate risk profiles and compliance matrices.

Part of the **CSOAI Governance Suite**: Provider Comparison + EU AI Act + GDPR + NIST AI RMF + ISO 42001.

[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-255+_servers-purple)](https://meok.ai)

## Tools

| Tool | Description |
|------|-------------|
| `compare_providers` | Compare providers against governance standards with scoring |
| `recommend_for_use_case` | Recommend most compliant LLM for a use case and jurisdiction |
| `provider_risk_profile` | Generate detailed risk profile for a specific provider |
| `compliance_matrix` | Show compliance matrix across providers and frameworks |
| `crosswalk_providers` | Map provider safety policies to CSOAI articles |

## Quick Start

```bash
pip install mcp
git clone https://github.com/CSOAI-ORG/llm-compliance-comparison-mcp.git
cd llm-compliance-comparison-mcp
python server.py
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "llm-compliance-comparison": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/llm-compliance-comparison-mcp"
    }
  }
}
```

## Provider Coverage

| Provider | Models | Safety Framework |
|----------|--------|-----------------|
| Anthropic | Claude 4 (Opus/Sonnet/Haiku) | Constitutional AI + RSP |
| OpenAI | GPT-4o / o1 / o3 | Preparedness Framework + Model Spec |
| Google DeepMind | Gemini 2.5 Pro/Flash/Ultra | AI Principles + Frontier Safety |
| Meta | Llama 4 (Scout/Maverick) | Open Model Safety + Responsible Use |
| Mistral AI | Mistral Large/Medium/Small | EU-based Moderation + Usage Policies |

## Frameworks Assessed

EU AI Act, GDPR, NIST AI RMF, ISO 42001, SOC 2, Canada AIDA -- plus CSOAI Partnership Charter crosswalk.

## The Decision Tool

Procurement teams and compliance officers can use `recommend_for_use_case` to get jurisdiction-aware, risk-rated provider recommendations. No other MCP server provides this.

## License

MIT -- see [LICENSE](LICENSE)
