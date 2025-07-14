import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

def map_assess_summary(bedrock_model):
    st.markdown("Upload a CSV or Excel file and generate an AWS environment summary.")
    uploaded_file = st.file_uploader("Upload infrastructure export File", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            file_name = uploaded_file.name.lower()
            if file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                csv_text = uploaded_file.getvalue().decode("utf-8")
            elif file_name.endswith((".xlsx", ".xls")):
                uploaded_file.seek(0)
                data = uploaded_file.read()
                df = pd.read_excel(BytesIO(data), engine="openpyxl")
                csv_text = df.to_csv(index=False)
            else:
                st.error("Unsupported file type.")
                st.stop()
        except Exception as e:
            st.error(f"Failed to read file: {e}")
            st.stop()

        if st.button("Generate Summary"):
            with st.spinner("Calling agent..."):
                prompt = f"""
                You are an AWS expert reviewing a infrastructure export CSV output.
                From this data, provide a high-level analysis:
                - What AWS services are in use?
                - Where is there high concentration or risk?
                - Are there any optimization opportunities?
                - Is the environment migration-ready?
                - Any missing components or blockers?
                Only answer based on the data below.
                --- CSV START ---
                {csv_text}
                --- CSV END ---
                """

                aws_docs_tool = MCPClient(
                    lambda: stdio_client(StdioServerParameters(
                        command="uvx", 
                        args=["awslabs.aws-documentation-mcp-server@latest"]))
                )
                agent = Agent(
                    name="MAPSummaryAgent", 
                    description="infrastructure export summary", 
                    model=bedrock_model, 
                    tools=[aws_docs_tool])
                response = agent(prompt)
                st.subheader("Summary")
                st.markdown(str(response).strip())
