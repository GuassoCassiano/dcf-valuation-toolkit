import sqlite3

DB_FILE = 'valuations.db'

print("\n--- Checking database ---")

try: 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM dcf_results'):
        print(row)

    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")
