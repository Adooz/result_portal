from flask import Flask, render_template, request, send_from_directory, redirect, flash
import os
from config import Config
from utils.file_helpers import load_json, save_json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'SECRET_KEY'  # Required for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    sessions = ["2023_2024", "2024_2025"]
    terms = ["First_Term", "Second_Term", "Third_Term"]
    
    if request.method == 'POST':
        access_code = request.form['access_code'].strip()
        student_id = request.form['student_id'].strip()
        session = request.form['session']
        term = request.form['term']

        access_codes = load_json(app.config['ACCESS_CODE_DB'])
        students = load_json(app.config['STUDENT_DB'])

        # Validate student ID
        student_info = students.get(student_id)
        if not student_info:
            flash("Student ID not found.")
            return redirect('/')

        # Validate access code existence and check if it is assigned to another student
        if access_code:
            if access_code not in access_codes:
                flash("Invalid access code.")
                return redirect('/')

            record = access_codes[access_code]
            assigned_to = record.get('assigned_to')

            # Access code assigned to another student
            if assigned_to and assigned_to != student_id:
                flash("Access code already assigned to another student.")
                return redirect('/')

        # Serve the result file
        student_class = student_info['class']
        result_path = os.path.join(app.config['RESULTS_FOLDER'], session, term, student_class)
        result_file = f"{student_id}.pdf"
        full_path = os.path.join(result_path, result_file)

        print("Looking for file at:", full_path)  # Debug print

        if not os.path.exists(full_path):
            flash("Result not found.")
            return redirect('/')  # Early exit if the result is not found

        # Handle case with no access code (assign access code if result is found)
        if not access_code:
            access_codes[student_id] = {"assigned_to": student_id, "usage_count": 0}
            save_json(app.config['ACCESS_CODE_DB'], access_codes)
            flash(f"Access code has been assigned to student {student_id}.")

        # At this point, the file exists — now update usage count
        if access_code:
            access_codes[access_code]['usage_count'] += 1
            save_json(app.config['ACCESS_CODE_DB'], access_codes)

        # Force PDF to be displayed inline
        response = send_from_directory(result_path, result_file, as_attachment=False, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename={result_file}'
        return response

    return render_template('index.html', sessions=sessions, terms=terms)

if __name__ == '__main__':
    app.run(debug=True)
