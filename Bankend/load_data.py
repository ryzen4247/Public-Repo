from database import get_connection

def load_sample_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Sample conversation
    cursor.execute("INSERT INTO conversations (user1, user2) VALUES (%s, %s)", ("Alice", "Bob"))
    conversation_id = cursor.lastrowid

    # Sample messages
    messages = [
        (conversation_id, "Alice", "Hey Bob!"),
        (conversation_id, "Bob", "Hey Alice! How are you?")
    ]
    cursor.executemany("INSERT INTO messages (conversation_id, sender, content) VALUES (%s, %s, %s)", messages)

    conn.commit()
    conn.close()
    print("Sample data loaded.")

if __name__ == "__main__":
    load_sample_data()
