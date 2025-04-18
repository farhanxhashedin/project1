from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from langgraph_workflow import graph, WorkflowState
import os
import uuid
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SRS to FastAPI Generator",
    description="Generates FastAPI projects from SRS documents using Groq/Llama3",
    version="1.0.0"
)

@app.post("/generate-project")
async def generate_project(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    try:
        # Validate file
        if not file.filename.endswith(".docx"):
            raise HTTPException(400, "Only .docx files supported")

        # Read and decode file content
        content = await file.read()
        srs_content = content.decode("utf-8")

        # Create initial state
        state = WorkflowState(
            srs_document=srs_content,
            iteration=0
        )

        # Run workflow
        result = graph.invoke(state)

        # Create project directory
        project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        project_dir = os.path.join("generated_projects", project_id)
        os.makedirs(project_dir, exist_ok=True)

        # Add background task for file generation
        if background_tasks:
            background_tasks.add_task(
                generate_project_files,
                project_dir,
                result["code"],
                result.get("tests", {})
            )

        return JSONResponse({
            "status": "processing",
            "project_id": project_id,
            "project_dir": project_dir,
            "preview": result["code"].get("main.py", "")
        })

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

def generate_project_files(project_dir: str, code: dict, tests: dict):
    """Generate project files in background"""
    try:
        # Create app directory structure
        app_dir = os.path.join(project_dir, "app")
        os.makedirs(app_dir, exist_ok=True)

        # Write main.py
        with open(os.path.join(app_dir, "main.py"), "w") as f:
            f.write(code.get("main.py", ""))

        # Write requirements.txt
        with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
            f.write("""fastapi>=0.68.0
uvicorn>=0.15.0
groq>=0.3.0
langgraph>=0.0.12
python-dotenv>=0.19.0
python-multipart>=0.0.5""")

        logger.info(f"Project generated at {project_dir}")

    except Exception as e:
        logger.error(f"File generation failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)