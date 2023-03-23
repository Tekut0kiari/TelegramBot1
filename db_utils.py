import sqlite3

def create_table(table_name):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, answer TEXT)")
    conn.commit()
    conn.close()

def insert_data(table_name, question, answer):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {table_name} (text, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def get_random_data(table_name):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result
