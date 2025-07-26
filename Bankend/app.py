from flask import Flask, jsonify
from database import get_connection

app = Flask(__name__)

# ✅ Function to fetch messages
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

# ✅ Function to fetch products
def fetch_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM products"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# 🏠 Home route
@app.route("/")
def home():
    return "Welcome to ChatBot API"

# 💬 Messages API
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = fetch_messages()
    return jsonify(messages)

# 🛒 Products API
@app.route("/products", methods=["GET"])
def get_products():
    products = fetch_products()
    return jsonify(products)

# 🚀 Run the app
if __name__ == "__main__":
    app.run(debug=True)
