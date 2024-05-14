import sqlite3
import requests


def fetch_cve_data(start_index, results_per_page):
    base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    params = {
        'startIndex': start_index,
        'resultsPerPage': results_per_page
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data['vulnerabilities']


def insert_cve_data_into_database(cve_data):
    conn = sqlite3.connect('cve_database.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS cves
                     (cve_id TEXT, description TEXT, severity TEXT, last_modified TEXT)''')

    for cve_item in cve_data:
        cve_id = cve_item['cve']['id']

        # Extract description
        if 'description' in cve_item['cve']:
            if 'descriptions' in cve_item['cve']['description']:
                description = cve_item['cve']['description']['descriptions'][0]['value']
            else:
                description = None
        else:
            description = None

        # Extract severity
        if 'impact' in cve_item and 'baseMetricV3' in cve_item['impact']:
            severity = cve_item['impact']['baseMetricV3']['cvssV3']['baseSeverity']
        else:
            severity = None

        # Extract last modified date
        if 'lastModifiedDateStr' in cve_item:
            last_modified = cve_item['lastModifiedDateStr']
        else:
            last_modified = None

        cursor.execute('''INSERT OR IGNORE INTO cves (cve_id, description, severity, last_modified) 
                          VALUES (?, ?, ?, ?)''', (cve_id, description, severity, last_modified))

    conn.commit()
    conn.close()


# Example usage
cve_data = fetch_cve_data(0, 10)
insert_cve_data_into_database(cve_data)
