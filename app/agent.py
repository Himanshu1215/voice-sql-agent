import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq

# Load .env from the project root, no matter where uvicorn is launched from
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DB_PATH = Path(__file__).parent.parent / "database" / "sales.db"
_agent = None

def build_agent():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            f"GROQ_API_KEY not found. Looked in env and {ENV_PATH}. "
            f".env exists: {ENV_PATH.exists()}"
        )
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=key)
    return create_sql_agent(
        llm=llm, db=db, agent_type="tool-calling",
        verbose=True, max_iterations=8,
    )

def ask(question: str) -> dict:
    global _agent
    if _agent is None:
        _agent = build_agent()
    result = _agent.invoke({"input": question})
    return {"question": question, "answer": result.get("output", "")}
