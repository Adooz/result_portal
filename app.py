from flask import Flask, render_template, request, send_from_directory, redirect, flash
import os
from config import Config
from utils.db import get_db_connection, init_db
from utils.file_helpers import load_json, save_json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'SECRET_KEY'  # Required for flashing messages

# Ensure necessary directories are created
def create_directories():
    # Create directories if they don't exist
    results_folder = os.path.join('/mnt/data', 'results')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

create_directories()

@app.route('/', methods=['GET', 'POST'])
def index():
    sessions = ["2023_2024", "2024_2025"]
    terms = ["First_Term", "Second_Term", "Third_Term"]
    
    if request.method == 'POST':
        access_code = request.form['access_code'].strip()
        student_id = request.form['student_id'].strip()
        session = request.form['session']
        term = request.form['term']

        # Load data from SQLite database
        conn = get_db_connection()
        c = conn.cursor()

        # Fetch student details
        c.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        student_info = c.fetchone()

        if not student_info:
            flash("Student ID not found.")
            return redirect('/')

        if access_code:
            c.execute("SELECT * FROM access_codes WHERE code = ?", (access_code,))
            record = c.fetchone()

            if not record:
                flash("Invalid access code.")
                return redirect('/')

            assigned_to = record[1]  # Access code assigned to student_id (index 1)

            # Access code assigned to another student
            if assigned_to and assigned_to != student_id:
                flash("Access code already assigned to another student.")
                return redirect('/')

            usage_count = record[2]  # Access code usage count (index 2)
            
            # Check if usage limit exceeded
            if usage_count >= 5:
                flash("Access code usage limit exceeded.")
                return redirect('/')

        # Serve the result file
        student_class = student_info[1]  # Class is in the second column of the student record
        result_path = os.path.join('/mnt/data', 'results', session, term, student_class)
        result_file = f"{student_id}.pdf"
        full_path = os.path.join(result_path, result_file)

        print("Looking for file at:", full_path)  # Debug print

        if not os.path.exists(full_path):
            flash("Result not found.")
            return redirect('/')  # Early exit if the result is not found

        # Handle case with no access code (assign access code if result is found)
        if not access_code:
            c.execute("INSERT OR REPLACE INTO access_codes (code, assigned_to, usage_count) VALUES (?, ?, ?)",
                      (student_id, student_id, 0))
            conn.commit()
            flash(f"Access code has been assigned to student {student_id}.")

        # Update usage count if access code is provided
        if access_code:
            c.execute("UPDATE access_codes SET usage_count = usage_count + 1 WHERE code = ?", (access_code,))
            conn.commit()

        # Force PDF to be displayed inline
        response = send_from_directory(result_path, result_file, as_attachment=False, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename={result_file}'
        return response

    return render_template('index.html', sessions=sessions, terms=terms)

if __name__ == '__main__':
    app.run(debug=True)
