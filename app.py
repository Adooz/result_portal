from flask import Flask, render_template, request, send_from_directory, redirect, flash
import os
import sqlite3
from config import Config
from utils.db import get_db_connection, init_app, init_db

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'SECRET_KEY'  # Required for flashing messages
init_app(app)


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

        # Validate access code if provided
        if access_code:
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
        result_path = os.path.join(app.config['RESULTS_FOLDER'], session, term, student_class)
        result_file = f"{student_id}.pdf"
        full_path = os.path.join(result_path, result_file)

        if not os.path.exists(full_path):
            flash("Result not found.")
            conn.close()
            return redirect('/')

        # If valid access code, update assignment and usage count
        if access_code:
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

if __name__ == '__main__':
    app.run(debug=True)
