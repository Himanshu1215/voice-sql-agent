# Voice to SQL Agent

Ask questions about a database **out loud** and get answers back in plain English.
Speech is transcribed by Whisper, converted to SQL by a LangChain agent, run
against SQLite, and the result is returned as natural language — all behind a
FastAPI service.

## Architecture

Voice (audio)
-> Whisper (speech-to-text)
-> LangChain SQL agent (natural language -> SQL)
-> SQLite (execute query)
-> LangChain (results -> plain English)
-> FastAPI response


## Tech stack

| Layer            | Technology                         |
|------------------|------------------------------------|
| Speech-to-text   | OpenAI Whisper (local)             |
| Agent            | LangChain SQL agent (tool-calling) |
| LLM              | Llama 3.3 70B via Groq             |
| Database         | SQLite (sample sales data)         |
| API              | FastAPI + Uvicorn                  |
| Containerisation | Docker                             |

## Database

A seeded sales database with four related tables:

- `customers` (200 rows) — name, country, region, signup date
- `products` (15 rows) — name, category, unit price, stock
- `orders` (1,000 rows) — customer, date, status
- `order_items` (~2,500 rows) — product and quantity per order

## Setup

```bash
# 1. Clone and enter
git clone <your-repo-url>
cd voice-sql-agent

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your free Groq API key (https://console.groq.com)
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Seed the database
python3 database/seed.py

# 6. Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Usage

Health check:

```bash
curl http://localhost:8000/
```

Ask a question as text:

```bash
curl -X POST http://localhost:8000/ask-text \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 3 products by total quantity sold?"}'
```

Ask a question by voice:

```bash
curl -X POST http://localhost:8000/ask-voice -F "audio=@question.mp3"
```

## Example

Question: *"What are the top 3 products by total quantity sold?"*

```json
{
  "question": "What are the top 3 products by total quantity sold?",
  "answer": "The top 3 products by total quantity sold are:\n1. Standing Desk - 588 units\n2. Webcam HD - 545 units\n3. Ergonomic Chair - 525 units"
}
```

## Docker

```bash
docker compose up --build
```

The API will be available at http://localhost:8000.

## Project structure

voice-sql-agent/
├── app/
│   ├── main.py        FastAPI app and endpoints
│   ├── agent.py       LangChain SQL agent
│   └── transcribe.py  Whisper speech-to-text
├── database/
│   └── seed.py        Creates and seeds sales.db
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


