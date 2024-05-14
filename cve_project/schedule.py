import sqlite3
import requests


def synchronize_cve_data():
    # Make API call to fetch CVE data
    response = requests.get('https://services.nvd.nist.gov/rest/json/cves/2.0')
    cve_data = response.json()

    # Process and update database
    #conn = sqlite3.connect('C:\Users\HP\OneDrive - Amrita Vishwa Vidyapeetham\Desktop\cve_project\cve_database.db')
    conn = sqlite3.connect(
        r'C:\Users\HP\OneDrive - Amrita Vishwa Vidyapeetham\Desktop\cve_project\cve_database.db')

    cursor = conn.cursor()

    # Insert or update CVE details in the database
    for cve in cve_data['CVE_Items']:
        cve_id = cve['cve']['CVE_data_meta']['ID']
        cve_description = cve['cve']['description']['description_data'][0]['value']
        cve_published_date = cve['publishedDate']
        cve_last_modified_date = cve['lastModifiedDate']
        cve_score = None
        if 'baseMetricV2' in cve['impact']:
            cve_score = cve['impact']['baseMetricV2']['cvssV2']['baseScore']
        elif 'baseMetricV3' in cve['impact']:
            cve_score = cve['impact']['baseMetricV3']['cvssV3']['baseScore']

        # Insert or replace CVE details into the database
        cursor.execute("INSERT OR REPLACE INTO cve_table (cve_id, description, published_date, last_modified_date, score) VALUES (?, ?, ?, ?, ?)",
                       (cve_id, cve_description, cve_published_date, cve_last_modified_date, cve_score))

    conn.commit()
    conn.close()
