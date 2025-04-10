import json
import sqlite3
import os
from config import Config

def import_students(json_path, db_path):
    with open(json_path, 'r') as f:
        students = json.load(f)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for student_id, details in students.items():
        student_class = details.get('class')
        student_name = details.get('name')  # Assuming 'name' is a key in the JSON file

        c.execute(
            "INSERT OR REPLACE INTO students (student_id, class, name) VALUES (?, ?, ?)",
            (student_id, student_class, student_name)
        )

    conn.commit()
    conn.close()
    print("✅ Students imported successfully.")

def import_access_codes(json_path, db_path):
    with open(json_path, 'r') as f:
        codes = json.load(f)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for code, details in codes.items():
        assigned_to = details.get('assigned_to')
        usage_count = details.get('usage_count', 0)

        c.execute(
            "INSERT OR REPLACE INTO access_codes (code, assigned_to, usage_count) VALUES (?, ?, ?)",
            (code, assigned_to, usage_count)
        )

    conn.commit()
    conn.close()
    print("✅ Access codes imported successfully.")

if __name__ == '__main__':
    DB_PATH = Config.DB_PATH
    STUDENT_JSON = os.path.join('data', 'students.json')
    ACCESS_CODE_JSON = os.path.join('data', 'access_codes.json')

    import_students(STUDENT_JSON, DB_PATH)
    import_access_codes(ACCESS_CODE_JSON, DB_PATH)
