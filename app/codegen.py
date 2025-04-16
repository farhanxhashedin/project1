from app.llama3_utils import call_llama3

def generate_code_from_parsed(parsed_data: str) -> str:
    prompt = f"""
You are an expert backend developer. Based on the following software requirements, generate a working FastAPI backend project with:

1. Pydantic models for data validation
2. API routes using FastAPI
3. SQLAlchemy models for PostgreSQL
4. Include `main.py` to register routes
5. Use clear folder structure (routers/, models/, schemas/, database/)

Requirements:
{parsed_data}

Only return code inside a ZIP-like structure or clearly labeled file sections, like:
"""
    return call_llama3(prompt)