# Flask CVE API

This is a Flask application that provides API endpoints to manage CVE (Common Vulnerabilities and Exposures) data using a PostgreSQL database.

## Setup

1. Install the required dependencies:
    ```bash
    pip install flask psycopg2-binary
    ```

2. Update the database connection parameters in `app.py` with your PostgreSQL credentials:
    ```python
    db_params = {
        'dbname': 'your_database_name',
        'user': 'your_username',
        'password': 'your_password',
        'host': 'your_host',
        'port': 'your_port'
    }
    ```

3. Set up the PostgreSQL database:
    ```sql
    CREATE DATABASE your_database_name;
    
    CREATE TABLE vulnerabilities (
        cve_id VARCHAR PRIMARY KEY,
        severity VARCHAR,
        cvss FLOAT,
        affected_packages TEXT,
        description TEXT,
        cwe_id VARCHAR
    );
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

## API Endpoints

### 1. Retrieve details of a particular CVE
- **URL:** `/cve/<cve_id>`
- **Method:** `GET`
- **Parameters:**
  - `<cve_id>`: Path parameter representing the CVE-ID to fetch.
- **Response:** Details of the CVE.

### 2. Retrieve all CVE data
- **URL:** `/cve/all`
- **Method:** `GET`
- **Parameters:** None
- **Response:** List of all CVEs.

### 3. Add a new CVE record
- **URL:** `/cve/addCVE`
- **Method:** `POST`
- **Payload:** JSON object with the details of the new CVE record.
- **Response:** Success or failure message.

### 4. Delete a CVE record
- **URL:** `/cve/<cve_id>`
- **Method:** `DELETE`
- **Parameters:**
  - `<cve_id>`: Path parameter representing the CVE-ID to delete.
- **Response:** Success or failure message.

### 5. Update a CVE record (Optional Bonus)
- **URL:** `/cve/<cve_id>`
- **Method:** `PUT`
- **Parameters:**
  - `<cve_id>`: Path parameter representing the CVE-ID to update.
  - **Payload:** JSON object with the updated details of the CVE.
- **Response:** Success or failure message.

## Error Handling

The application handles errors such as missing fields, invalid CVE IDs, and database connection issues by returning appropriate error responses.

