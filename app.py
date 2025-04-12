from flask import Flask, render_template, request, send_from_directory, redirect, flash
import os
import sqlite3
from config import Config
from utils.db import get_db_connection, init_app, init_db
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'SECRET_KEY'  # Required for flashing messages
init_app(app)

DB_PATH = os.path.join(os.getcwd(), 'result_portal.db')  # SQLite database location
MASTER_ACCESS_CODE = "universal"  # Master PIN with unlimited usage

def add_timestamp_to_pdf(original_pdf_path):
    # Create a new PDF in memory to overlay the timestamp
    timestamp_pdf = BytesIO()
    c = canvas.Canvas(timestamp_pdf, pagesize=letter)

    # Format the timestamp: "Day of week, Day Month Year at Time"
    timestamp = datetime.now().strftime('%A, %d %B %Y at %I:%M %p')

    # Set the font and size for the timestamp
    c.setFont("Helvetica", 10)

    # Calculate the width of the timestamp text
    text_width = c.stringWidth(timestamp, "Helvetica", 10)
    page_width = letter[0]  # Width of the page in points (letter size: 8.5" x 11")

    # Calculate the x position to ensure the timestamp is aligned to the right
    x_position = page_width - text_width - 20  # 20 points from the right edge for padding

    # Shift 2 cm (56.69 points) to the left from the current position
    x_position -= 56.69  # Shift by 2 cm (56.69 points)

    # Position the timestamp in the top-right corner (adjust y-coordinate if necessary)
    c.drawString(x_position, 770, f"Printed on: {timestamp}")  # Adjust the y-coordinate to your needs

    c.save()

    # Move the timestamp PDF to the beginning of the original PDF
    timestamp_pdf.seek(0)
    timestamp_pdf_reader = PdfReader(timestamp_pdf)
    original_pdf_reader = PdfReader(original_pdf_path)
    pdf_writer = PdfWriter()

    # Add the timestamp overlay to each page of the original PDF
    for page_num in range(len(original_pdf_reader.pages)):
        page = original_pdf_reader.pages[page_num]
        page.merge_page(timestamp_pdf_reader.pages[0])  # Merge the timestamp overlay with the original page
        pdf_writer.add_page(page)

    # Save the modified PDF to a temporary file
    modified_pdf_path = original_pdf_path.replace(".pdf", "_Result.pdf")
    with open(modified_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    return modified_pdf_path

@app.route('/', methods=['GET', 'POST'])
def index():
    sessions = ["2023_2024", "2024_2025"]
    terms = ["First_Term", "Second_Term", "Third_Term"]

    if request.method == 'POST':
        access_code = request.form['access_code'].strip()
        student_id = request.form['student_id'].strip()
        session = request.form['session']
        term = request.form['term']

        if term == "#":
            flash("Please select a correct term.", "error")
            return redirect('/')

        conn = get_db_connection()

        # Validate student ID
        student = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
        if not student:
            flash("Exam Number not found.")
            conn.close()
            return redirect('/')

        # Check if master code is used
        is_master_code = (access_code == MASTER_ACCESS_CODE)

        # Validate access code from DB (unless it's master code)
        if access_code and not is_master_code:
            code = conn.execute("SELECT * FROM access_codes WHERE code = ?", (access_code,)).fetchone()
            if not code:
                flash("Invalid PIN.")
                conn.close()
                return redirect('/')

            assigned_to = code['assigned_to']
            usage_count = code['usage_count']

            if assigned_to and assigned_to != student_id:
                flash("PIN already assigned to another student.")
                conn.close()
                return redirect('/')

            if usage_count >= 5:
                flash("PIN usage limit exceeded.")
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

        # Add timestamp to the PDF
        modified_pdf_path = add_timestamp_to_pdf(full_path)

        # Display the modified PDF inline
        flash("Result downloaded!.")
        response = send_from_directory(result_path, os.path.basename(modified_pdf_path), as_attachment=False, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename={os.path.basename(modified_pdf_path)}'
        return response

    return render_template('index.html', sessions=sessions, terms=terms)

if __name__ == '__main__':
    app.run(debug=True)
