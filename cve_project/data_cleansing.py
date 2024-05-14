import sqlite3

conn = sqlite3.connect('cve_database.db')
cursor = conn.cursor()

# Identify duplicates
cursor.execute('''SELECT cve_id, COUNT(*)
                  FROM cves
                  GROUP BY cve_id
                  HAVING COUNT(*) > 1''')
duplicates = cursor.fetchall()

# Remove duplicates
for cve_id, count in duplicates:
    cursor.execute('''DELETE FROM cves
                      WHERE rowid NOT IN (SELECT MIN(rowid)
                                          FROM cves
                                          WHERE cve_id = ?
                                          GROUP BY cve_id)''', (cve_id,))

# Identify missing values
cursor.execute('''SELECT *
                  FROM cves
                  WHERE severity IS NULL OR description IS NULL OR last_modified IS NULL''')
missing_values = cursor.fetchall()

# Handle missing values
# 1.Deleting rows with missing values
for row in missing_values:
    cve_id = row[0]
    cursor.execute('''DELETE FROM cves WHERE cve_id = ?''', (cve_id,))
    
# 2.Updating missing values
for row in missing_values:
    cve_id = row[0]
    cursor.execute(
        '''UPDATE cves SET severity = ? WHERE cve_id = ?''', ('Unknown', cve_id))

# 3.Imputation:-Impute missing values with the mean, median, or mode of the respective column.
for row in missing_values:
    cve_id = row[0]
    # Replace missing severity with the mean severity
    cursor.execute(
        '''UPDATE cves SET severity = (SELECT AVG(severity) FROM cves WHERE severity IS NOT NULL) WHERE cve_id = ?''', (cve_id,))

