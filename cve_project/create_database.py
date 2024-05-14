import sqlite3

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('cve_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store CVE information
cursor.execute('''CREATE TABLE IF NOT EXISTS cves (
                    cve_id TEXT PRIMARY KEY,
                    description TEXT,
                    severity TEXT,
                    last_modified TEXT
                  )''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and table created successfully.")
