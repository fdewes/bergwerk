from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    file = FileField('Upload JSON File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class ConfigForm(FlaskForm):
    error_message = StringField('Error Message', validators=[DataRequired()])
    initial_greeting = TextAreaField('Initial Greeting', validators=[DataRequired()])
    inactivity_timer = StringField('Inactivity Timer', validators=[DataRequired()])
    English_llm_models_training_list = TextAreaField('LLM Models Training List', validators=[DataRequired()])
    English_llm_models_training_instruction = TextAreaField('LLM Training Instruction', validators=[DataRequired()])
    
    update_config = SubmitField('Update Configuration')

    # Mapping of fields for easy retrieval in app.py
    fields = {
        "error_message": error_message,
        "initial_greeting": initial_greeting,
        "inactivity_timer": inactivity_timer,
        "English_llm_models_training_list": English_llm_models_training_list,
        "English_llm_models_training_instruction": English_llm_models_training_instruction
    }
