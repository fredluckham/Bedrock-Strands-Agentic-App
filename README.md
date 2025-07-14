# AWS Agentic Tools

This is a modular Streamlit application that integrates with the AWS Strands SDK and Model Context Protocol (MCP) servers to provide intelligent cloud tooling and visualizations. It allows users to upload AWS MAP/ASSESS outputs, generate architecture diagrams using natural language, and receive migration guidance — all powered by Bedrock-hosted foundation models and official AWS documentation MCP servers.

## Features

### 1. MAP/ASSESS Summary
Upload a CSV or Excel file generated from an AWS MAP or Assess phase. The tool:
- Parses the input
- Summarizes key services, patterns, and risks
- Suggests AWS best practices for modernization or migration

### 2. AWS Diagram Generator
Enter a freeform description of your AWS architecture. The tool:
- Uses a Bedrock-powered agent and the AWS Diagram MCP server
- Returns a visual architecture in Mermaid format
- Renders the diagram directly in the app

### 3. Migration & Optimization Advisor
Describe your current infrastructure and goals. The tool:
- Analyzes the environment using the AWS Documentation MCP server
- Suggests appropriate AWS services and migration paths
- Offers potential cost guidance based on standard pricing

## Prerequisites

- Python 3.10+
- AWS credentials with access to Bedrock (for Claude or other foundation models)
- AWS CLI configured with the appropriate region
- https://docs.astral.sh/uv/

## Installation

1. Clone the repo and install dependencies:

```bash
uv sync
```

2. Run the Streamlit app:

```bash
streamlit run main.py
```

## File Structure

```
aws_agentic_tools/
├── main.py
├── map_assess_summary.py
├── diagram_generator.py
├── migration_advisor.py
```

- `main.py`: The entry point with the sidebar view selector
- `map_assess_summary.py`: Handles CSV/XLSX uploads and agent summaries
- `diagram_generator.py`: Prompts an agent to create Mermaid diagrams
- `migration_advisor.py`: Uses documentation MCP to generate migration suggestions

## Configuration

The Bedrock model ID and region are defined at the top of `main.py`. Modify as needed:

```python
BEDROCK_MODEL_ID = "anthropic.claude-3-7-sonnet-20250219-v1:0"
AWS_REGION = "eu-west-2"
```

## License

This project is intended for educational and internal consulting use. Refer to AWS service terms and the license of the Strands SDK for redistribution or commercial use.
