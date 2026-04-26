import sqlite3

conn = sqlite3.connect('data/healthcare_gold.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Get schema for each table
for table in tables:
    print(f"\nSchema for {table[0]}:")
    cursor.execute(f"PRAGMA table_info({table[0]})")
    print(cursor.fetchall())
    
    # Get sample data
    print(f"\nSample data from {table[0]}:")
    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
    print(cursor.fetchall())

conn.close()