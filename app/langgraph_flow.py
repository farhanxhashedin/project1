from langgraph.graph import StateGraph, END
from app.llama3_utils import call_llama3

# Define state structure
class GraphState(dict):
    pass

# Define node
def parse_srs_node(state: GraphState) -> GraphState:
    srs_text = state["srs_text"]
    prompt = f"""You are an expert software engineer. Read the following Software Requirement Spec (SRS) and extract:
1. Functional Requirements
2. API endpoints (name, method, description, input/output)
3. Database schema
4. Business logic

SRS Document:
{srs_text}
"""
    structured_output = call_llama3(prompt)
    return {"parsed_data": structured_output}

# Build graph
def build_langgraph():
    builder = StateGraph(GraphState)
    builder.add_node("parse_srs", parse_srs_node)
    builder.set_entry_point("parse_srs")
    builder.set_finish_point("parse_srs")
    return builder.compile()
