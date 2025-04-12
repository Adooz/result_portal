from flask import Flask, render_template, request, send_from_directory, redirect, flash
import os
import sqlite3
from config import Config
from utils.db import get_db_connection, init_app, init_db

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'SECRET_KEY'  # Required for flashing messages
init_app(app)

DB_PATH = os.path.join(os.getcwd(), 'result_portal.db')  # SQLite database location
MASTER_ACCESS_CODE = "Adoozisback1@"  # Master PIN with unlimited usage

@app.route('/', methods=['GET', 'POST'])
def index():
    sessions = ["2023_2024", "2024_2025"]
    terms = ["First_Term", "Second_Term", "Third_Term"]

    if request.method == 'POST':
        access_code = request.form['access_code'].strip()
        student_id = request.form['student_id'].strip()
        session = request.form['session']
        term = request.form['term']

        conn = get_db_connection()

        # Validate student ID
        student = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
        if not student:
            flash("Student ID not found.")
            conn.close()
            return redirect('/')

        # Check if master code is used
        is_master_code = (access_code == MASTER_ACCESS_CODE)

        # Validate access code from DB (unless it's master code)
        if access_code and not is_master_code:
            code = conn.execute("SELECT * FROM access_codes WHERE code = ?", (access_code,)).fetchone()
            if not code:
                flash("Invalid access code.")
                conn.close()
                return redirect('/')

            assigned_to = code['assigned_to']
            usage_count = code['usage_count']

            if assigned_to and assigned_to != student_id:
                flash("Access code already assigned to another student.")
                conn.close()
                return redirect('/')

            if usage_count >= 5:
                flash("Access code usage limit exceeded.")
                conn.close()
                return redirect('/')

        # Check if result file exists
        student_class = student['class']
        student_name = student['name']
        result_path = os.path.join(app.config['RESULTS_FOLDER'], session, term, student_class)
        result_file = f"{student_name}.pdf"
        full_path = os.path.join(result_path, result_file)

        if not os.path.exists(full_path):
            flash("Result not found.")
            conn.close()
            return redirect('/')

        # Update usage only for normal access codes
        if access_code and not is_master_code:
            conn.execute("""
                UPDATE access_codes
                SET assigned_to = ?, usage_count = usage_count + 1
                WHERE code = ?
            """, (student_id, access_code))
            conn.commit()

        conn.close()

        # Display the PDF inline
        response = send_from_directory(result_path, result_file, as_attachment=False, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename={result_file}'
        return response

    return render_template('index.html', sessions=sessions, terms=terms)

@app.route('/debug/tables')
def show_tables():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return {'tables': [t[0] for t in tables]}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/debug/table/<table_name>')
def view_table_data(table_name):
    try:
        limit = request.args.get('limit', default=100, type=int)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        if not cursor.fetchone():
            return {'error': f"Table '{table_name}' does not exist"}, 404

        cursor.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]

        conn.close()
        return {'table': table_name, 'limit': limit, 'rows': data}

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
