from wtforms import Form, StringField, SelectField
from wtforms.validators import DataRequired

class ResultForm(Form):
    access_code = StringField('Access Code', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    session = SelectField('Academic Session', choices=[('2023_2024', '2023_2024'), ('2024_2025', '2024_2025')], validators=[DataRequired()])
    term = SelectField('Term', choices=[('First_Term', 'First Term'), ('Second_Term', 'Second Term'), ('Third_Term', 'Third Term')], validators=[DataRequired()])
