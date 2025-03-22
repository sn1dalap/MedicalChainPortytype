import sqlite3

def init_db():
    conn = sqlite3.connect('medical_blockchain.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  block_index INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

def add_patient(name, block_index):
    conn = sqlite3.connect('medical_blockchain.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, block_index) VALUES (?, ?)", (name, block_index))
    conn.commit()
    conn.close()

def get_patient_block_index(name):
    conn = sqlite3.connect('medical_blockchain.db')
    c = conn.cursor()
    c.execute("SELECT block_index FROM patients WHERE name = ?", (name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None