import streamlit as st
import os
from strands.models import BedrockModel
from map_assess_summary import map_assess_summary
from diagram_generator import diagram_generator
from migration_advisor import migration_advisor

os.environ["AWS_REGION"] = "eu-west-2"
BEDROCK_MODEL_ID = "anthropic.claude-3-7-sonnet-20250219-v1:0"

bedrock_model = BedrockModel(
    model_id=BEDROCK_MODEL_ID,
    region_name="eu-west-2",
    temperature=0.3,
)

st.set_page_config(page_title="AWS Agentic Tools", layout="wide")
st.title("AWS Agentic Tools")

view = st.sidebar.radio("Choose a view:", ["MAP/ASSESS Summary", "AWS Diagram Generator", "Migration & Optimization Advisor"])

if view == "MAP/ASSESS Summary":
    map_assess_summary(bedrock_model)
elif view == "AWS Diagram Generator":
    diagram_generator(bedrock_model)
elif view == "Migration & Optimization Advisor":
    migration_advisor(bedrock_model)
