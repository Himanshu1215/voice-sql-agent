import os, tempfile, shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app import transcribe as stt
from app import agent as sql_agent

app = FastAPI(title="Voice to SQL Agent", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class TextQuery(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "ok", "service": "voice-to-sql-agent"}

@app.post("/ask-text")
def ask_text(query: TextQuery):
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty.")
    return sql_agent.ask(query.question)

@app.post("/ask-voice")
async def ask_voice(audio: UploadFile = File(...)):
    suffix = os.path.splitext(audio.filename or "")[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name
    try:
        question = stt.transcribe(tmp_path)
        result = sql_agent.ask(question)
        result["transcript"] = question
        return result
    finally:
        os.unlink(tmp_path)
