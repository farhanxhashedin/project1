import os
from fastapi import FastAPI, File, UploadFile
from tempfile import NamedTemporaryFile
from app.parsers.docx_parser import parse_docx
from app.langgraph_flow import build_langgraph

app = FastAPI()
graph = build_langgraph()

@app.post("/upload-srs")
async def upload_srs(file: UploadFile = File(...)):
    if file.filename.endswith(".docx") is False:
        return {"error": "Only .docx files supported"}

    with NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text = parse_docx(tmp_path)
        result = graph.invoke({"srs_text": text})
        os.remove(tmp_path)
        return {"structured_output": result["parsed_data"]}
    except Exception as e:
        return {"error": str(e)}
