from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from tools import search_notes, generate_quiz
from memory_store import add_memory
from pypdf import PdfReader

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    text = ""

    if file.filename.endswith(".pdf"):
        pdf = PdfReader(file.file)
        for page in pdf.pages:
            text += page.extract_text() or ""
    else:
        content = await file.read()
        text = content.decode("utf-8")

    add_memory(text)
    return {"message": "Uploaded successfully"}

@app.get("/ask")
def ask(query: str):
    results = search_notes(query)

    if not results:
        return {"results": ["No relevant data found"]}

    content = " ".join(results)
    q = query.lower()

    if "name" in q or "person" in q:
        lines = content.split("\n")
        names = [line for line in lines if "Team" in line or "Name" in line]
        return {"results": names if names else ["No names found"]}

    elif "about" in q or "what" in q:
        return {"results": [content[:400]]}

    return {"results": [content[:500]]} 

@app.get("/quiz")
def quiz(topic: str):
    notes = search_notes(topic)
    content = " ".join(notes)
    return {"quiz": generate_quiz(content)}