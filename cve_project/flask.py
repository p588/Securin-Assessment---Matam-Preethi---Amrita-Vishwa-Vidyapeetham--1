from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/cves', methods=['GET'])
def get_cve_details():
    # Connect to the SQLite database
    conn = sqlite3.connect('C:\Users\HP\OneDrive - Amrita Vishwa Vidyapeetham\Desktop\cve_project\cve_database.db')
    cursor = conn.cursor()

    # Execute a query to retrieve the CVE details
    cursor.execute("SELECT * FROM cve_table")

    # Fetch all rows
    cve_rows = cursor.fetchall()

    # Process the retrieved data
    cve_details = []
    for row in cve_rows:
        cve_detail = {
            'cve_id': row[0],
            'description': row[1],
            'published_date': row[2],
            'last_modified_date': row[3],
            'score': row[4]
        }
        cve_details.append(cve_detail)

    # Close the database connection
    conn.close()

    # Return the data as JSON
    return jsonify(cve_details)


if __name__ == '__main__':
    app.run(debug=True)
