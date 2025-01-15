import sqlite3

# Connect to SQLite
conn = sqlite3.connect('air_quality.db')
cursor = conn.cursor()

# Create a table for air quality data
cursor.execute('''
CREATE TABLE IF NOT EXISTS air_quality (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    city TEXT,
    aqi INTEGER,
    pm2_5 REAL,
    pm10 REAL,
    co REAL,
    no2 REAL,
    o3 REAL,
    so2 REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Database initialized successfully.")
