from langgraph.graph import StateGraph
from groq import Groq
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import os
import json
import logging

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "llama3-70b-8192"

    def generate(self, prompt: str) -> str:
        if not self.client:
            return json.dumps({"error": "Groq client not initialized"})
        
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.3
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return json.dumps({"error": str(e)})

class WorkflowState(BaseModel):
    srs_document: str = ""
    requirements: Dict[str, Any] = Field(default_factory=dict)
    project_structure: Dict[str, Any] = Field(default_factory=dict)
    code: Dict[str, Any] = Field(default_factory=dict)
    tests: Dict[str, Any] = Field(default_factory=dict)
    feedback: List[str] = Field(default_factory=list)
    iteration: int = 0

def get_llm():
    if os.getenv("GROQ_API_KEY"):
        return GroqClient()
    logger.warning("Using mock LLM - set GROQ_API_KEY for real responses")
    class MockLLM:
        def generate(self, prompt):
            return json.dumps({
                "api_endpoints": [{"name": "health", "method": "GET"}],
                "database_models": [{"name": "User", "attributes": []}],
                "project_structure": {"app": ["main.py"], "tests": []}
            })
    return MockLLM()

def extract_code(response: str) -> str:
    try:
        if "```python" in response:
            return response.split("```python")[1].split("```")[0].strip()
        return response.split("```")[1].strip() if "```" in response else response.strip()
    except:
        return response

def analyze_srs(state: WorkflowState) -> dict:
    logger.info("Analyzing SRS document")
    llm = get_llm()
    
    prompt = f"""Analyze this SRS document and extract structured requirements:
    {state.srs_document[:3000]}... [truncated]
    
    Return JSON with:
    - api_endpoints: list of endpoints with methods
    - database_models: list of data models
    - project_structure: suggested folder structure
    
    Output MUST be valid JSON only, no markdown formatting."""
    
    try:
        response = llm.generate(prompt)
        return {"requirements": json.loads(response)}
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM response")
        return {"requirements": {}}

def generate_structure(state: WorkflowState) -> dict:
    logger.info("Generating project structure")
    llm = get_llm()
    
    prompt = f"""Create FastAPI project structure for:
    {json.dumps(state.requirements, indent=2)}
    
    Return JSON structure with 'app' and 'tests' directories.
    Include essential files like main.py and requirements.txt."""
    
    try:
        response = llm.generate(prompt)
        return {"project_structure": json.loads(response)}
    except json.JSONDecodeError:
        logger.error("Failed to parse structure response")
        return {"project_structure": {}}

def generate_code(state: WorkflowState) -> dict:
    logger.info("Generating code")
    llm = get_llm()
    code = {}
    
    # Generate main.py
    prompt = f"""Create FastAPI main.py for these requirements:
    {json.dumps(state.requirements, indent=2)}
    
    Include:
    - FastAPI app initialization
    - Basic health endpoint
    - Proper CORS configuration
    
    Return only Python code in ```python block"""
    
    try:
        response = llm.generate(prompt)
        code["main.py"] = extract_code(response)
    except Exception as e:
        code["main.py"] = "from fastapi import FastAPI\n\napp = FastAPI()"
    
    return {"code": code}

# Build LangGraph workflow
workflow = StateGraph(WorkflowState)

workflow.add_node("analyze_srs", analyze_srs)
workflow.add_node("generate_structure", generate_structure)
workflow.add_node("generate_code", generate_code)

workflow.set_entry_point("analyze_srs")
workflow.add_edge("analyze_srs", "generate_structure")
workflow.add_edge("generate_structure", "generate_code")

graph = workflow.compile()