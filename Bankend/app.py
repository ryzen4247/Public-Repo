from database import get_connection

def fetch_messages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT m.id, m.content, m.sender, m.timestamp, c.user1, c.user2
    FROM messages m
    JOIN conversations c ON m.conversation_id = c.id
    ORDER BY m.timestamp ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    chats = fetch_messages()
    for msg in chats:
        print(f"[{msg['timestamp']}] {msg['sender']}: {msg['content']}")
from flask import Flask, jsonify
from database import get_connection

app = Flask(__name__)

# Your existing function
def fetch_messages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT m.id, m.content, m.sender, m.timestamp, c.user1, c.user2
    FROM messages m
    JOIN conversations c ON m.conversation_id = c.id
    ORDER BY m.timestamp ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# 🧪 Test API route
@app.route("/")
def home():
    return "Welcome to ChatBot API"

# 🔁 New API route to get messages
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = fetch_messages()
    return jsonify(messages)

# ✅ Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
