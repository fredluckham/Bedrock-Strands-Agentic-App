import streamlit as st
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

def migration_advisor(bedrock_model):
    st.markdown("Describe your current setup. The agent will suggest migration paths, AWS services, and cost estimates.")
    user_description = st.text_area("Describe your environment and goals")

    if st.button("Get AWS Migration Advice"):
        if not user_description.strip():
            st.warning("Please provide a description.")
            st.stop()

        with st.spinner("Analyzing..."):
            aws_docs_tool = MCPClient(
                lambda: stdio_client(StdioServerParameters(
                    command="uvx", 
                    args=["awslabs.aws-documentation-mcp-server@latest"]))
            )

            agent = Agent(
                name="MigrationAdvisorAgent", 
                description="Migration + cost guidance", 
                model=bedrock_model, 
                tools=[aws_docs_tool])
            
            prompt = f"""
            You are an AWS cloud architect and cost optimization specialist.
            Given this environment, suggest:
            - AWS services and architecture
            - Migration path (lift-and-shift, replatform, refactor)
            - Optimization opportunities
            - Monthly AWS cost estimate
            Use 2025 AWS pricing and answer only based on input.
            --- INPUT START ---
            {user_description}
            --- INPUT END ---
            """
            
            response = agent(prompt)
            st.subheader("Migration & Optimization Advice")
            st.markdown(str(response).strip())
