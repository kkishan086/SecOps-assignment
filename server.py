from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Get database parameters from environment variables
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except psycopg2.Error as e:
        return None

# Error handler for 404 Not Found
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

# API Endpoints

@app.route('/cve/<cve_id>', methods=['GET'])
def get_cve(cve_id):
    conn = get_db_connection()
    if conn is None:
        return internal_server_error("Unable to connect to the database.")
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM vulnerabilities WHERE cve_id = %s', (cve_id,))
    cve = cursor.fetchone()
    conn.close()
    if cve:
        return jsonify(cve), 200
    else:
        return resource_not_found(f"CVE-ID {cve_id} not found")

@app.route('/cve/all', methods=['GET'])
def get_all_cves():
    conn = get_db_connection()
    if conn is None:
        return internal_server_error("Unable to connect to the database.")
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM vulnerabilities')
    cves = cursor.fetchall()
    conn.close()
    return jsonify(cves), 200

@app.route('/cve/addCVE', methods=['POST'])
def add_cve():
    new_cve = request.get_json()
    cve_id = new_cve.get('cve_id')
    severity = new_cve.get('severity')
    cvss = new_cve.get('cvss')
    affected_packages = new_cve.get('affected_packages')
    description = new_cve.get('description')
    cwe_id = new_cve.get('cwe_id')
    
    if not all([cve_id, severity, cvss, affected_packages, description, cwe_id]):
        return bad_request("Missing required fields")
    
    conn = get_db_connection()
    if conn is None:
        return internal_server_error("Unable to connect to the database.")
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO vulnerabilities (cve_id, severity, cvss, affected_packages, description, cwe_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (cve_id) DO NOTHING
        ''', (cve_id, severity, cvss, affected_packages, description, cwe_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return internal_server_error(str(e))
    conn.close()
    return jsonify({"message": "CVE added successfully"}), 201

@app.route('/cve/<cve_id>', methods=['DELETE'])
def delete_cve(cve_id):
    conn = get_db_connection()
    if conn is None:
        return internal_server_error("Unable to connect to the database.")
    
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vulnerabilities WHERE cve_id = %s', (cve_id,))
    if cursor.rowcount == 0:
        conn.close()
        return resource_not_found(f"CVE-ID {cve_id} not found")
    conn.commit()
    conn.close()
    return jsonify({"message": "CVE deleted successfully"}), 200

@app.route('/cve/<cve_id>', methods=['PUT'])
def update_cve(cve_id):
    updated_cve = request.get_json()
    fields = ["severity", "cvss", "affected_packages", "description", "cwe_id"]
    set_clause = ', '.join([f"{field} = %s" for field in fields if field in updated_cve])
    values = [updated_cve[field] for field in fields if field in updated_cve] + [cve_id]
    
    if not set_clause:
        return bad_request("No valid fields to update")
    
    conn = get_db_connection()
    if conn is None:
        return internal_server_error("Unable to connect to the database.")
    
    cursor = conn.cursor()
    cursor.execute(sql.SQL(f'''
    UPDATE vulnerabilities
    SET {set_clause}
    WHERE cve_id = %s
    '''), values)
    
    if cursor.rowcount == 0:
        conn.close()
        return resource_not_found(f"CVE-ID {cve_id} not found")
    
    conn.commit()
    conn.close()
    return jsonify({"message": "CVE updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
