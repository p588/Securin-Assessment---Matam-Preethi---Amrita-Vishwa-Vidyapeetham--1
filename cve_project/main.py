import time
import requests
import json
import sqlite3


def get_cves(start_index, results_per_page):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?startIndex={start_index}&resultsPerPage={results_per_page}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:  # Handle rate limiting
        print(f"Rate limit reached! Sleeping for 10 seconds...")
        time.sleep(10)  # Adjust delay based on NVD API rate limits
        return get_cves(start_index, results_per_page)  # Retry after delay
    else:
        raise Exception(f"Error retrieving CVEs: {response.status_code}")


def store_cves(cves):
    conn = sqlite3.connect("cve_data.db")
    cursor = conn.cursor()

    # Create table with appropriate data types (adjust as needed)
    cursor.execute("""CREATE TABLE IF NOT EXISTS cves (
        cve_id TEXT PRIMARY KEY,
        published_date TEXT,
        lastModifiedDate TEXT,
        description TEXT,
        cvss_v2_score REAL,
        cvss_v3_score REAL
    )""")

    for cve in cves.get("results", []):
        data = (
            cve["cve_id"],
            cve["publishedDate"],
            cve["lastModifiedDate"],
            cve["description"]["description_data"][0]["value"],
            cve.get("impact", {}).get("baseMetricV2", {}).get(
                "cvssData", {}).get("baseScore"),
            cve.get("impact", {}).get("baseMetricV3", {}).get(
                "cvssData", {}).get("baseScore"),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO cves VALUES (?, ?, ?, ?, ?, ?)", data)

    conn.commit()
    conn.close()


def main():
    start_index = 0
    results_per_page = 50  # Adjust as needed

    while True:
        cves = get_cves(start_index, results_per_page)
        if not cves.get("totalResults", 0):
            break

        store_cves(cves)
        start_index += results_per_page


if __name__ == "__main__":
    main()
