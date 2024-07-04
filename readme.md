# Flask CVE API

This is a Flask application that provides API endpoints to manage CVE (Common Vulnerabilities and Exposures) data using a PostgreSQL database.

## File Structure

my_python_app/
│
├── cve_psql_db_setup.py
├── .env
├── CVE_DATABASE.csv
├── server.py
└── README.md

- `cve_psql_db_setup.py`: Script to set up the PostgreSQL database.
- `.env`: Environment variables file containing configuration such as database credentials.
- `CVE_DATABASE.csv`: CSV file containing the data to be loaded into the database.
- `server.py`: Script to run the server.

## Setup

1. Install the required dependencies:
    ```bash
    pip install flask psycopg2-binary python-dotenv os
    ```

2. Update the database connection parameters in `.env` with your PostgreSQL credentials:
   ```bash
      DB_NAME=your_database_name
      DB_USER=your_username
      DB_PASSWORD=your_password
      DB_HOST=your_host
      DB_PORT=your_port
    ```

3. Set up the PostgreSQL database for CVE's:
- Run this command:
    ```bash
    python cve_psql_db_steup.py

    ````

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


