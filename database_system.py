import sqlite3
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Database setup
def setup_database():
    conn = sqlite3.connect('data_tracing.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Insert data
def insert_data(data):
    conn = sqlite3.connect('data_tracing.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO records (data) VALUES (?)', (data,))
    conn.commit()
    conn.close()

# Trace data for the last 5 years
def trace_data():
    conn = sqlite3.connect('data_tracing.db')
    cursor = conn.cursor()
    five_years_ago = datetime.now() - timedelta(days=5*365)
    cursor.execute('SELECT * FROM records WHERE timestamp >= ?', (five_years_ago,))
    records = cursor.fetchall()
    conn.close()
    return records

# View all data
def view_data():
    conn = sqlite3.connect('data_tracing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM records')
    records = cursor.fetchall()
    conn.close()
    return records

# Search data
def search_data(search_term):
    conn = sqlite3.connect('data_tracing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM records WHERE data LIKE ?', ('%' + search_term + '%',))
    records = cursor.fetchall()
    conn.close()
    return records

# Delete data
def delete_data(record_id):
    conn = sqlite3.connect('data_tracing.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Export to PDF
def export_to_pdf(records):
    c = canvas.Canvas("data_records.pdf", pagesize=letter)
    c.drawString(100, 750, "Data Records")
    y = 730
    for record in records:
        c.drawString(100, y, f"ID: {record[0]}, Data: {record[1]}, Timestamp: {record[2]}")
        y -= 20
    c.save()

# Setup database
setup_database()
