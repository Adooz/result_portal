from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ResultCheckForm(FlaskForm):
    student_id = StringField("Student ID", validators=[DataRequired()])
    access_code = StringField("Access Code", validators=[DataRequired()])
    
    session = SelectField(
        "Session",
        choices=[("2023_2024", "2023/2024"), ("2024_2025", "2024/2025")],
        validators=[DataRequired()]
    )
    
    term = SelectField(
        "Term",
        choices=[("First_Term", "First Term"), ("Second_Term", "Second Term"), ("Third_Term", "Third Term")],
        validators=[DataRequired()]
    )
    
    submit = SubmitField("Check Result")
