import streamlit as st
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from streamlit_mermaid import st_mermaid

def sanitize_mermaid(mermaid: str) -> str:
    lines = mermaid.strip().splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    if not lines[0].startswith(("graph", "flowchart", "sequenceDiagram", "classDiagram")):
        lines.insert(0, "graph TD")
    return "\n".join(lines)

def diagram_generator(bedrock_model):
    st.markdown("Describe an architecture or workload, and the agent will generate a Mermaid diagram.")
    description = st.text_area("Describe your AWS architecture")

    if st.button("Generate Diagram"):
        if not description.strip():
            st.warning("Please provide a description.")
            st.stop()

        with st.spinner("Generating diagram..."):
            diagram_tool = MCPClient(
                lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.aws-diagram-mcp-server@latest"]))
            )
            agent = Agent(name="DiagramAgent", description="Creates AWS architecture diagrams", model=bedrock_model, tools=[diagram_tool])

            prompt = f"""You are an AWS architect. Create a Mermaid diagram only, with no explanation.

            The input description is:

            """
            {description}
            """

            Respond only with a valid Mermaid diagram.
            """

            response = agent(prompt)
            mermaid_code = str(response).replace("```mermaid", "").replace("```", "").strip()
            mermaid_code = sanitize_mermaid(mermaid_code)

            st.subheader("Architecture Diagram")
            st_mermaid(mermaid_code)
            with st.expander("📄 View Raw Mermaid Code"):
                st.code(mermaid_code, language="markdown")
