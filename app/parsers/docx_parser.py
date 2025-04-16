import docx2txt

def parse_docx(file_path: str) -> str:
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        raise ValueError(f"Error parsing .docx: {e}")
