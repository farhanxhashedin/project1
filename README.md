

---

# 🛠️ SRS to FastAPI Generator

Generate FastAPI project scaffolding from a `.docx` SRS (Software Requirements Specification) using **Groq Llama3** and **LangGraph**. This tool helps developers bootstrap a backend project quickly from a functional document.

---

## 🚀 Features

- Upload `.docx` SRS files to generate project boilerplate
- Automatically analyzes requirements, APIs, and models using LLMs
- Generates:
  - `main.py` with FastAPI app setup
  - Project folder structure
  - `requirements.txt`
- Uses **LangGraph** to orchestrate multi-step workflows
- Built with **FastAPI**, **Groq Llama3**, and **LangGraph**

---

## 📦 Project Structure

```
srs-fastapi-generator/
├── app/
│   └── main.py          # Generated FastAPI app entry point
├── generated_projects/  # Output folder for generated projects
├── langgraph_workflow.py# LangGraph workflow logic
├── main.py              # FastAPI backend API
├── .env                 # Contains GROQ_API_KEY
└── requirements.txt     # Project dependencies
```

---

## 📄 API Endpoints

### `POST /generate-project`

Upload a `.docx` SRS document to generate a FastAPI project.

**Request:**
- `file`: `.docx` file (multipart/form-data)

**Response:**
```json
{
  "status": "processing",
  "project_id": "project_20250418010000",
  "project_dir": "generated_projects/project_20250418010000",
  "preview": "# FastAPI code preview..."
}
```

---

### `GET /health`

Health check for the API.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/srs-fastapi-generator.git
cd srs-fastapi-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add `.env` File

Create a `.env` file with your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

### 4. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

Go to [http://localhost:8000/docs](http://localhost:8000/docs) to test via Swagger UI.

---

## 🧠 How It Works

1. **Analyze SRS**: Extract API endpoints, models, and structure from the uploaded document using LLM.
2. **Generate Structure**: Build directory and file structure for the project.
3. **Generate Code**: Create a basic FastAPI app based on extracted requirements.
4. **Save Files**: Files are saved in the `generated_projects/` folder.

---

## 🤖 Powered By

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Groq LLM (LLaMA 3)](https://console.groq.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

---

## 🧪 Future Improvements

- Support for PDF and plaintext SRS files
- Add support for generating test cases
- UI for uploading and previewing project
- GitHub integration to auto-push generated projects

---


Let me know if you want the README to include screenshots, setup instructions for Docker, or auto-deploy to GitHub Pages / Render!
