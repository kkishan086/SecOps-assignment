import csv
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
# Define the path to the CSV file
csv_file_path = 'CVE_DATABASE.csv' 

# Get database parameters from environment variables
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Create the table schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS vulnerabilities (
    cve_id TEXT PRIMARY KEY,
    severity TEXT,
    cvss REAL,
    affected_packages TEXT,
    description TEXT,
    cwe_id TEXT
)
''')

# Function to read the CSV file and insert data into the database
def import_csv_to_db(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cursor.execute('''
            INSERT INTO vulnerabilities (cve_id, severity, cvss, affected_packages, description, cwe_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (cve_id) DO NOTHING
            ''', (
                row['CVE-ID'],
                row['Severity'],
                float(row['CVSS']),
                row['Affected Packages'],
                row['Description'],
                row['CWE-ID']
            ))
        conn.commit()

# Import the CSV data into the database
import_csv_to_db(csv_file_path)

# Close the database connection
conn.close()

print(f"Data imported successfully into PostgreSQL database")
