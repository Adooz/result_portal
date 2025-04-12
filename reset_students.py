import sqlite3
import pandas as pd
from config import Config

DB_PATH = Config.DATABASE

def drop_and_create_students_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop the students table if it exists
    cur.execute("DROP TABLE IF EXISTS students")

    # Recreate the students table
    cur.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            class TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Dropped and recreated 'students' table.")

def load_students_from_file(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    if not {'student_id', 'name', 'class'}.issubset(df.columns):
        raise ValueError("Missing required columns: student_id, name, class")

    return df

def populate_students(df):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO students (student_id, name, class) VALUES (?, ?, ?)",
            (row['student_id'], row['name'], row['class'])
        )
    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} students.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scripts/reset_students.py <path_to_file.csv/xlsx>")
        exit(1)

    file_path = sys.argv[1]
    try:
        drop_and_create_students_table()
        students_df = load_students_from_file(file_path)
        populate_students(students_df)
    except Exception as e:
        print("Error:", e)
