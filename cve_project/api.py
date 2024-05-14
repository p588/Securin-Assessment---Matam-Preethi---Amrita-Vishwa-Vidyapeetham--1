from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Database connection details (replace with yours)
DB_NAME = "cve_data.db"


def get_cve_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cves")
    count = cursor.fetchone()[0]
    conn.close()

    return count


def get_cves(page_size, page_num, sort_field=None, sort_order="ASC"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    order_by = f"{sort_field} {sort_order}" if sort_field else ""

    # Pagination logic (adjust as needed)
    offset = (page_num - 1) * page_size
    query = f"SELECT * FROM cves ORDER BY {order_by} LIMIT {page_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows


@app.route('/cves/list')
def get_cve_list():
    page_size = int(request.args.get('page_size', 10))  # Default 10 per page
    page_num = int(request.args.get('page_num', 1))  # Default to page 1
    sort_field = request.args.get('sort_field')
    sort_order = request.args.get('sort_order', 'ASC')

    cves = get_cves(page_size, page_num, sort_field, sort_order)
    total_count = get_cve_count()

    return jsonify({
        "cves": [dict(zip(cursor.description[1:], row)) for row in cves],
        "total_count": total_count,
        "page_size": page_size,
        "page_num": page_num,
        "sort_field": sort_field,
        "sort_order": sort_order,
    })


if __name__ == "__main__":
    app.run(debug=True)
