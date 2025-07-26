
```python
# backend/app.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Tuple
import sqlite3
import requests
import uuid

app = FastAPI()

# 1. Database setup: create sessions and messages tables if not exist
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect("chat.db", check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            sender TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    """)
    return conn

# 2. Request model: message, optional conversation_id and user_id
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = "default"

# 3. LLM integration settings (replace with chosen API/key)
LLM_API_KEY = "YOUR_API_KEY"
LLM_ENDPOINT  = "https://api.groq.com/v1/chat/completions"

# 4. Call LLM: include history, ask clarifying questions if needed
def call_llm(history: List[Tuple], user_message: str) -> str:
    # build messages list for API
    msgs = [
        {
            "role": "user" if row[2]=="user" else "assistant",
            "content": row[3]
        }
        for row in history
    ]
    msgs.append({"role": "user", "content": user_message})
    headers = {"Authorization": f"Bearer {LLM_API_KEY}"}
    payload = {"model": "llama3-70b-8192", "messages": msgs}
    resp = requests.post(LLM_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    # simple clarifier: if LLM hints unclear, prepend question
    if "clarify" in content.lower() and "?" not in user_message:
        return "Can you clarify? " + content
    return content

# 5. API endpoint: POST /api/chat
@app.post("/api/chat")
def chat_endpoint(body: ChatRequest):
    conn = get_db()
    cur  = conn.cursor()

    # session management: create new session if none provided
    sess_id = body.conversation_id or str(uuid.uuid4())
    if not body.conversation_id:
        cur.execute(
            "INSERT INTO sessions (id, user_id) VALUES (?, ?)",
            (sess_id, body.user_id)
        )
        conn.commit()

    # save user message
    cur.execute(
        "INSERT INTO messages (session_id, sender, message) VALUES (?, 'user', ?)",
        (sess_id, body.message)
    )
    conn.commit()

    # fetch full history for this session
    cur.execute(
        "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
        (sess_id,)
    )
    history = cur.fetchall()

    # generate AI response
    ai_resp = call_llm(history, body.message)

    # save AI response
    cur.execute(
        "INSERT INTO messages (session_id, sender, message) VALUES (?, 'ai', ?)",
        (sess_id, ai_resp)
    )
    conn.commit()
    conn.close()

    # return conversation_id and AI reply
    return {"conversation_id": sess_id, "response": ai_resp}

# To run: uvicorn backend.app:app --reload
```
